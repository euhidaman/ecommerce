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
      console.log("User is Authenticated, sending data...")
    }

  })
}
