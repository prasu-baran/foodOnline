$(document).ready(function() {
    // Function to load cart details
    function loadCartDetails() {
        $.ajax({
            type: 'GET',
            url: '/cart-details', // Replace with your endpoint to fetch cart details
            success: function(response) {
                if (response.status === 'Success') {
                    // Update cart counter
                    $('#cart_counter').html(response.cart_counter['cart_count']);

                    // Apply cart amounts
                    applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax_dict'], response.cart_amount['grand_total']);

                    // Update quantities for items
                    response.cart_items.forEach(item => {
                        $('#qty-' + item.food_id).html(item.qty);
                    });

                    // Handle empty cart scenario
                    if (response.cart_counter['cart_count'] === 0 && window.location.pathname === '/cart') {
                        $('#menu-item-list-6272 ul').html('<div class="text-center p-5"><h3>Cart is empty</h3></div>');
                    }
                }
            },
            error: function() {
                console.error("Failed to load cart details.");
            }
        });
    }

    // Call loadCartDetails when the page loads
    loadCartDetails();

    // Add to cart
    $('.add_to_cart').off('click').on('click', function(e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = { food_id: food_id };

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                if (response.status === 'login_required') {
                    Swal.fire({
                        title: 'Login Required',
                        text: response.message,
                        icon: 'info',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Login Now'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location = '/login';
                        }
                    });
                } else if (response.status === 'Failed') {
                    Swal.fire({
                        title: 'Error!',
                        text: response.message,
                        icon: 'error',
                        confirmButtonColor: '#3085d6'
                    });
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);
                    applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax_dict'], response.cart_amount['grand_total']);
                }
            }
        });
    });

    // Decrease cart
    $('.decrease_cart').off('click').on('click', function(e) {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = { food_id: food_id };
        var thisItem = $(this).closest('li');

        $.ajax({
            type: 'GET',
            url: url,
            data: data,
            success: function(response) {
                if (response.status === 'login_required') {
                    Swal.fire({
                        title: 'Login Required',
                        text: response.message,
                        icon: 'info',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Login Now'
                    }).then((result) => {
                        if (result.isConfirmed) {
                            window.location = '/login';
                        }
                    });
                } else if (response.status === 'Failed') {
                    Swal.fire({
                        title: 'Error!',
                        text: response.message,
                        icon: 'error',
                        confirmButtonColor: '#3085d6'
                    });
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);
                    applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax_dict'], response.cart_amount['grand_total']);

                    if (response.qty <= 0 && window.location.pathname === '/cart') {
                        thisItem.remove();

                        if ($('#menu-item-list-6272 ul li').length === 0) {
                            $('#menu-item-list-6272 ul').html('<div class="text-center p-5"><h3>Cart is empty</h3></div>');
                        }
                    }
                }
            }
        });
    });

    // Delete cart item
    $('.delete_cart').off('click').on('click', function(e) {
        e.preventDefault();
    
        var cart_id = $(this).attr('data-id'); // Get the cart item ID
        var url = $(this).attr('data-url');   // Get the URL for the delete request
        var thisItem = $(this).closest('li'); // Identify the cart item element in the DOM
    
        Swal.fire({
            title: 'Are you sure?',
            text: "You want to remove this item from the cart?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, remove it!'
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: 'GET',
                    url: url,
                    success: function(response) {
                        if (response.status === 'Success') {
                            // Remove the cart item element from the DOM
                            if (window.location.pathname === '/cart') {
                                thisItem.remove();
                            }
    
                            // Update the cart counter
                            $('#cart_counter').html(response.cart_counter['cart_count']);
    
                            // Update the cart amounts (subtotal, tax, total)
                            applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax_dict'], response.cart_amount['grand_total']);
    
                            // Show success message
                            Swal.fire(
                                'Deleted!',
                                'Item has been removed from the cart.',
                                'success'
                            );
    
                            // Check if the cart is now empty
                            if ($('#menu-item-list-6272 ul li').length === 0 && window.location.pathname === '/cart') {
                                $('#menu-item-list-6272 ul').html('<div class="text-center p-5"><h3>Cart is empty</h3></div>');
                            }
                        } else if (response.status === 'login_required') {
                            Swal.fire({
                                title: 'Login Required',
                                text: response.message,
                                icon: 'info',
                                showCancelButton: true,
                                confirmButtonColor: '#3085d6',
                                cancelButtonColor: '#d33',
                                confirmButtonText: 'Login Now'
                            }).then((result) => {
                                if (result.isConfirmed) {
                                    window.location = '/login';
                                }
                            });
                        } else {
                            Swal.fire(
                                'Error!',
                                response.message,
                                'error'
                            );
                        }
                    },
                    error: function(xhr, status, error) {
                        Swal.fire(
                            'Error!',
                            'Something went wrong! Please try again.',
                            'error'
                        );
                    }
                });
            }
        });
    });

    function applyCartAmounts(subtotal, tax_dict, grand_total) {
        $('#subtotal').html(subtotal);
        console.log(tax_dict)
        $('#total').html(grand_total);
        for(key1 in tax_dict){
            for(key2 in tax_dict[key1]){
                $('#tax-'+key1).html(tax_dict[key1][key2])
                
            }
        }
    }
  //document ready
  // Use event delegation for the add_hour button
  $(document).on('click', '.remove_hour', function(e) {
    e.preventDefault();

    const url = $(this).attr('data-url'); // Get the URL for removing the opening hour
    const row = $(this).closest('tr');   // Identify the table row for this item

    $.ajax({
        type: 'GET',
        url: url,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
        success: function(response) {
            if (response.status === 'success') {
                // Remove the row with a fade-out animation
                row.fadeOut(300, function() {
                    $(this).remove(); // Completely remove the row after the fade-out
                });

                Swal.fire({
                    title: 'Success!',
                    text: 'Opening hour removed successfully.',
                    icon: 'success',
                    confirmButtonColor: '#3085d6',
                });
            } else {
                Swal.fire({
                    title: 'Error!',
                    text: response.message || 'Failed to remove the opening hour.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6',
                });
            }
        },
        error: function(xhr) {
            Swal.fire({
                title: 'Error!',
                text: 'Failed to remove the opening hour. Please try again.',
                icon: 'error',
                confirmButtonColor: '#3085d6',
            });
        }
    });
});


// Add opening hours form handler
$('#opening-hours').on('submit', function(e) {
    e.preventDefault();
    const url = $('#add_hour_url').val();
    const formData = new FormData(this);

    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
        success: function(response) {
            if (response.status === 'success') {
                location.reload();
            }
        }
    });
});
 

  $(document).ready(function() {
    $('.add_hour').on('click', function (e) {
        e.preventDefault();
        
        var form = $('#opening-hours');
        var day = $('#id_day').val();
        var from_hour = $('#id_from_hour').val();
        var to_hour = $('#id_to_hour').val();
        var is_closed = $('#id_is_closed').is(':checked') ? 'True' : 'False';
        var csrf_token = form.find('input[name=csrfmiddlewaretoken]').val();
        var url = $('#add_hour_url').val();
        
        if (!day || (!is_closed && (!from_hour || !to_hour))) {
            Swal.fire({
                text: 'Please fill in all required details.',
                icon: 'info',
                confirmButtonColor: '#3085d6',
            });
            return;
        }

        $.ajax({
            type: 'POST',
            url: url,
            data: {
                'day': day,
                'from_hour': from_hour,
                'to_hour': to_hour,
                'is_closed': is_closed,
                'csrfmiddlewaretoken': csrf_token
            },
            success: function (response) {
                if (response.status === 'success') {
                    // Create the time display string
                    var timeDisplay = response.is_closed ? 
                        'Closed' : 
                        `${response.from_hour}-${response.to_hour}`;
                    
                    // Create new row using response data
                    var html = `
                        <tr id="hour-${response.id}">
                            <td><b>${response.day}</b></td>
                            <td>${timeDisplay}</td>
                            <td><a href="#"class='remove_hour'data-url="/vendor/opening-hour/remove/"+response.id+>Remove</a></td>
                        </tr>
                    `;
                    
                    // Append new row
                    $('.opening_hours tbody').append(html);
                    
                    // Reset form
                    $('#opening-hours')[0].reset();

                    // Show success message
                    Swal.fire({
                        title: 'Success!',
                        text: 'Opening hours added successfully',
                        icon: 'success',
                        confirmButtonColor: '#3085d6',
                    });
                } else {
                    Swal.fire({
                        title: 'Error!',
                        text: response.error || 'An error occurred',
                        icon: 'error',
                        confirmButtonColor: '#3085d6',
                    });
                }
            },
            error: function (xhr, status, error) {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error!',
                    text: 'Failed to add the opening hour. Please try again.',
                    icon: 'error',
                    confirmButtonColor: '#3085d6',
                });
            }
        });
    });
});


});



