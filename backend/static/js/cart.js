/* Set rates + misc */
var taxRate = 0.05;
var shippingRate = 15.00;
var fadeTime = 300;


var amount = 0;
$(document).ready(function () {
  recalculateCart();
  var total = document.getElementById('cart-total').innerHTML;

  console.log(total)
});

document.onload
/* Assign actions */
$('.product-quantity input').change(function () {
  updateQuantity(this);
});


/* Recalculate cart */
function recalculateCart() {
  var subtotal = 0;

  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });

  /* Calculate totals */
  var tax = subtotal * taxRate;
  var shipping = (subtotal > 0 ? shippingRate : 0);
  var total = subtotal + tax + shipping;
  amount = total
  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function () {
    $('#cart-subtotal').html(subtotal.toFixed(2));
    $('#cart-tax').html(tax.toFixed(2));
    $('#cart-shipping').html(shipping.toFixed(2));
    $('#cart-total').html(total.toFixed(2));
    if (total == 0) {
      $('.checkout').fadeOut(fadeTime);
    } else {
      $('.checkout').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });
}


/* Update quantity */
function updateQuantity(quantityInput) {
  /* Calculate line price */
  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children('.product-price').text());
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;

  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function () {
      $(this).text(linePrice.toFixed(2));
      recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });
}


/* Remove item from cart */
function removeItem(removeButton) {
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeButton).parent().parent();
  productRow.slideUp(fadeTime, function () {
    productRow.remove();
    recalculateCart();
  });
}






var checkout = document.getElementById('chec');

var quan = document.getElementsByClassName('quantity')
var a = document.querySelectorAll('.product-title')

for (var i = 0; i < quan.length; i++) {
  quan[i].onchange = function () {
    var quantities = []
    var item_ids = []
    for (var i = 0; i < quan.length; i++) {
      item_ids.push(a[i].dataset.id)
      quantities.push(quan[i].value)
    }
    update_cart(item_ids, quantities)
  }
}

checkout.addEventListener('click', function () {
  console.log(amount)
  order_create(amount)
  var visible = document.getElementById('visible')
  visible.style.visibility="hidden"

})


function update_cart(item_ids, quantities) {
  var url = 'update_cart'

  fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ 'item_ids': item_ids, 'quantities': quantities })
  })
    .then((response) => {
      
      if (response.ok) {
        console.log('ok')
      }
      else {
        alert('not sucess')
      }
      return response.json()
    })
    .then((data)=>{
      if(data != 'working'){
        alert("quantity exceeding limit")
      }

    })


}



function order_create(amount) {
  var url = 'order_create'

  fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      "X-CSRFToken": csrftoken
    },
    body: JSON.stringify({ 'amount': amount })
  })
    .then((response) => {
      if (response.ok) {
        window.location.replace('checkout');
      }
      else {
        alert('error')
      }
    })

}





















var remove = document.getElementsByClassName('remove-product')

for (var i = 0; i < remove.length; i++) {

  remove[i].addEventListener('click', function () {
    var item_id = this.dataset.id
    console.log('id', item_id)
    let x = removefromcart(item_id)
    setTimeout(() => { removeItem(this); }, 500);



  })
}

function removefromcart(item_id) {

  fetch('remove_from_user_cart', {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({ 'item_id': item_id })
  })

    .then((response) => {
      console.log('hi')
    })

}