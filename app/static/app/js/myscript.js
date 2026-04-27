
$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// Helper function to get CSRF token from meta tag
function getCSRFToken() {
    return $('meta[name="csrf-token"]').attr('content');
}

$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    $.ajax({
        type:"POST",
        url:"/pluscart/",
        data:{
            prod_id:id,
            csrfmiddlewaretoken: getCSRFToken()
        },
        success:function(data)
        {
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount.toFixed(2)
            document.getElementById("total_amount").innerText=data.total_amount.toFixed(2)
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml=this.parentNode.children[2]
    $.ajax({
        type:"POST",
        url:"/minuscart/",
        data:{
            prod_id:id,
            csrfmiddlewaretoken: getCSRFToken()
        },
        success:function(data)
        {
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount.toFixed(2)
            document.getElementById("total_amount").innerText=data.total_amount.toFixed(2)
        }
    })
})

$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"POST",
        url:"/removecart/",
        data:{
            prod_id:id,
            csrfmiddlewaretoken: getCSRFToken()
        },
        success:function(data)
        {
            if (data.status === 'success') {
                document.getElementById("amount").innerText=data.amount.toFixed(2)
                document.getElementById("total_amount").innerText=data.total_amount.toFixed(2)
                $(eml).closest('.cart-item').fadeOut(300, function() {
                    $(this).remove();
                    if ($('.cart-item').length === 0) {
                        location.reload(); // Reload to show empty cart message
                    }
                });
            } else if (data.status === 'empty') {
                location.reload();
            }
        }
    })
})