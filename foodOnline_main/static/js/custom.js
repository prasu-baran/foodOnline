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
                console.log(error);
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
                    if (response.qty <= 0 && window.location.pathname === '/cart/') {
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

                            console.log(response)
                            // Show success message
                            Swal.fire(
                                'Deleted!',
                                'Item has been removed from the cart.',
                                'success'
                            );
    
                            // Check if the cart is now empty
                            if (response.cart_counter['cart_count'] == 0  && window.location.pathname === '/cart/') {
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

    // ===== FAVOURITE TOGGLE =====
    $(document).on('click', '.toggle-favourite', function(e) {
        e.preventDefault();
        var url = $(this).attr('data-url');
        var icon = $(this).find('i');
        var btn = $(this);
        $.ajax({
            type: 'GET',
            url: url,
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                if (response.status === 'login_required') {
                    Swal.fire({ title: 'Login Required', text: response.message, icon: 'info',
                        showCancelButton: true, confirmButtonText: 'Login Now' })
                        .then(function(r) { if (r.isConfirmed) window.location = '/login'; });
                } else if (response.status === 'added') {
                    icon.removeClass('fa-heart-o').addClass('fa-heart text-danger');
                    btn.attr('title', 'Remove from favourites');
                    Swal.fire({ toast: true, position: 'top-end', icon: 'success',
                        title: response.message, showConfirmButton: false, timer: 1500 });
                } else if (response.status === 'removed') {
                    icon.removeClass('fa-heart text-danger').addClass('fa-heart-o');
                    btn.attr('title', 'Add to favourites');
                    Swal.fire({ toast: true, position: 'top-end', icon: 'info',
                        title: response.message, showConfirmButton: false, timer: 1500 });
                }
            }
        });
    });

    // ===== COUPON APPLY =====
    $(document).on('click', '#apply-coupon-btn', function(e) {
        e.preventDefault();
        var code = $('#coupon-code').val().trim();
        if (!code) { $('#coupon-msg').html('<span class="text-danger">Please enter a coupon code.</span>'); return; }
        $.ajax({
            type: 'POST',
            url: $(this).attr('data-url'),
            data: { coupon_code: code, csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').first().val() },
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                if (response.status === 'success') {
                    $('#coupon-msg').html('<span class="text-success">' + response.message + '</span>');
                    $('#total').html(parseFloat(response.final_total).toFixed(2));
                } else {
                    $('#coupon-msg').html('<span class="text-danger">' + response.message + '</span>');
                }
            }
        });
    });

    // ===== COUPON REMOVE =====
    $(document).on('click', '#remove-coupon-btn', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: $(this).attr('data-url'),
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                if (response.status === 'success') { location.reload(); }
            }
        });
    });

    // ===== USE SAVED ADDRESS at Checkout =====
    $(document).on('click', '.use-saved-address', function(e) {
        e.preventDefault();
        $('input[name=address], textarea[name=address]').val($(this).data('address'));
        $('input[name=city]').val($(this).data('city'));
        $('input[name=state]').val($(this).data('state'));
        $('input[name=country]').val($(this).data('country'));
        $('input[name=pin_code]').val($(this).data('pincode'));
        Swal.fire({ toast: true, position: 'top-end', icon: 'success',
            title: 'Address filled!', showConfirmButton: false, timer: 1200 });
    });

    // ===== REVIEW FORM on vendor_detail page =====
    $(document).on('submit', '#review-form', function(e) {
        e.preventDefault();
        var url = $(this).find('button[type=submit]').attr('data-url');
        var rating = $(this).find('input[name=rating]:checked').val();
        var comment = $(this).find('textarea[name=comment]').val();
        var csrf = $(this).find('input[name=csrfmiddlewaretoken]').val();
        if (!rating) { Swal.fire({ icon: 'warning', text: 'Please select a star rating.', confirmButtonColor: '#dc3545' }); return; }
        $.ajax({
            type: 'POST', url: url,
            data: { rating: rating, comment: comment, csrfmiddlewaretoken: csrf },
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                if (response.status === 'success') {
                    Swal.fire({ icon: 'success', title: response.message, confirmButtonColor: '#dc3545' })
                        .then(function() { location.reload(); });
                } else {
                    Swal.fire({ icon: 'error', text: response.message, confirmButtonColor: '#dc3545' });
                }
            }
        });
    });

    // ===== INLINE REVIEW FORM on order_detail page =====
    $(document).on('submit', '.review-form-inline', function(e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('data-url');
        var rating = form.find('input[name=rating]:checked').val();
        var comment = form.find('textarea[name=comment]').val();
        var csrf = form.find('input[name=csrfmiddlewaretoken]').val();
        if (!rating) { Swal.fire({ icon: 'warning', text: 'Please select a star rating.', confirmButtonColor: '#dc3545' }); return; }
        $.ajax({
            type: 'POST', url: url,
            data: { rating: rating, comment: comment, csrfmiddlewaretoken: csrf },
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            success: function(response) {
                if (response.status === 'success') {
                    Swal.fire({ icon: 'success', title: response.message, confirmButtonColor: '#dc3545' });
                    form.find('button[type=submit]').text('Update Review');
                } else {
                    Swal.fire({ icon: 'error', text: response.message, confirmButtonColor: '#dc3545' });
                }
            }
        });
    });

    // ===== STAR RATING hover effect =====
    $(document).on('mouseover', '.review-stars label, .review-stars-inline label', function() {
        $(this).css('color', '#f8a401').nextAll('label').css('color', '#f8a401');
    }).on('mouseout', '.review-stars label, .review-stars-inline label', function() {
        var form = $(this).closest('form');
        var checked = form.find('input[name=rating]:checked');
        form.find('.review-stars label, .review-stars-inline label').css('color', '#ccc');
        if (checked.length) { checked.next('label').css('color', '#f8a401').nextAll('label').css('color', '#f8a401'); }
    });

});


