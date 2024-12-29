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
                    applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax'], response.cart_amount['grand_total']);

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
                    applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax'], response.cart_amount['grand_total']);
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
                    applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax'], response.cart_amount['grand_total']);

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
                            applyCartAmounts(response.cart_amount['subtotal'], response.cart_amount['tax'], response.cart_amount['grand_total']);
    
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

    function applyCartAmounts(subtotal, tax, grand_total) {
        $('#subtotal').html(subtotal);
        $('#tax').html(tax);
        $('#total').html(grand_total);
    }
});
