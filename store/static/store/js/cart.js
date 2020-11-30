// query all the elements in html code, tht has the class 'update-cart'
var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i<updateBtns.length ; i++)
{
  updateBtns[i].addEventListener('click', function(){
    // 'this' keyword in javascript is actually similar to
    // python's __self__ method.
    // it represents the item , tht is clicked on
    var productId = this.dataset.product
    // above code takes the 'product' from data-product(product.id)
    var action = this.dataset.action
    // above code takes the 'action' from data-action(add)
    console.log('productId: ', productId, 'action: ',action)

    console.log('USER: ', user);
    if(user == 'AnonymousUser'){
      console.log("User not Authenticated")
    }
    else {
        updateUserOrder(productId, action)
    }
  })
}


function updateUserOrder(productId, action){
  console.log('User is Authenticated, sending data...')
  var url = '/update_item/'

  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    // the below 'body' is being sent as a JSON string to 'updateItem' view in views.py
    body:JSON.stringify({'productId':productId, 'action':action})
  })
  .then((response) =>{
    return response.json();
  })
  .then((data) =>{
    console.log('Data:',data)
    //below line is written, to refresh the page to increment the cart total in red on top right corner
    location.reload()
  })
}
