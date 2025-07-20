const successMessage = document.getElementById("jq-notification");
const btnAddToCart = document.querySelectorAll(".add-to-cart");
const btnRemoveFromCart = document.querySelectorAll(".remove-from-cart");
const goodsInCartCount = document.getElementById("goods-in-cart-count");
const goodsInCartCountMain = document.getElementById("goods-in-cart-count-main");
const orderBtn = document.getElementById("orderBtn");
const goodsInCartCountModal = document.getElementById("goods-in-cart-count-modal");
const cartItemsContainer = document.getElementById("cart-items-container");//
const cartItemsContainerModal = document.getElementById("cart-items-container-modal");//
const deleteOrder = document.getElementById("delete_order");

function displayActionMessage(data) {
  const message = data.message;
  successMessage.innerHTML = message;
  successMessage.style.display = "block";

  // Через 3сек убираем сообщение
  setTimeout(function () {
    successMessage.style.display = "none";
  }, 3000);
}

btnAddToCart.forEach((el) => {
  el.addEventListener("click", async (e) => {
    e.preventDefault();

    let cartCount = parseInt(goodsInCartCountMain.textContent || 0);


    // Получаем id товара из атрибута data-product-id
    const product_id = el.dataset.productId;

    // Из атрибута href берем ссылку на контроллер django
    const add_to_cart_url = el.getAttribute("href");

    const data = {
      product_id: product_id,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    };

     $.ajax({
       type: "POST",
       url: add_to_cart_url,
       data: data,
       success: function (data) {
         cartCount++;
         goodsInCartCountMain.textContent = cartCount;
         //goodsInCartCountSmall.textContent = cartCount;
         goodsInCartCountModal.textContent = cartCount;

         displayActionMessage(data);
         console.log(data)
         // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)

         cartItemsContainerModal.innerHTML = data.cart_items_html;

         if (cartCount > 0) {
            orderBtn.classList.remove('invisible')
            goodsInCartCountMain.classList.remove('invisible')
         }
        
       },
     });
  });
});



// Ловим собыитие клика по кнопке удалить товар из корзины
$(document).on("click", ".remove-from-cart", function (e) {
  // Блокируем его базовое действие
  e.preventDefault();

  // Берем элемент счетчика в значке корзины и берем оттуда значение
  let cartCount = parseInt(goodsInCartCountMain.textContent || 0);

  // Получаем id корзины из атрибута data-cart-id
  var cart_id = $(this).data("cart-id");
  // Из атрибута href берем ссылку на контроллер django
  var remove_from_cart = $(this).attr("href");

  // делаем post запрос через ajax не перезагружая страницу
  $.ajax({
    type: "POST",
    url: remove_from_cart,
    data: {
      cart_id: cart_id,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {
      // Сообщение
      displayActionMessage(data);

      // Уменьшаем количество товаров в корзине (отрисовка)
      cartCount -= data.quantity_deleted;
      goodsInCartCountMain.textContent = cartCount;
      goodsInCartCountModal.textContent = cartCount;

      // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)

      cartItemsContainerModal.innerHTML = data.cart_items_html;
      deleteOrder.innerHTML = data.cart_items_html_1;
      cartItemsContainer.innerHTML = data.cart_items_html_1;
      if (cartCount == 0) {
            orderBtn.classList.add('invisible')
            goodsInCartCountMain.classList.add('invisible')
         }
    },
  });
});

// Теперь + - количества товара
// Обработчик события для уменьшения значения
$(document).on("click", ".decrement", function () {
  // Берем ссылку на контроллер django из атрибута data-cart-change-url
  var url = $(this).data("cart-change-url");
  // Берем id корзины из атрибута data-cart-id
  var cartID = $(this).data("cart-id");
  // Ищем ближайшеий input с количеством
  var $input = $(this).closest(".input-group").find(".number");
  // Берем значение количества товара
  var currentValue = parseInt($input.val());
  // Если количества больше одного, то только тогда делаем -1
  if (currentValue > 1) {
    $input.val(currentValue - 1);
    // Запускаем функцию определенную ниже
    // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
    updateCart(cartID, currentValue - 1, -1, url);
  }
});

// Обработчик события для увеличения значения
$(document).on("click", ".increment", function () {
  // Берем ссылку на контроллер django из атрибута data-cart-change-url
  var url = $(this).data("cart-change-url");
  // Берем id корзины из атрибута data-cart-id
  var cartID = $(this).data("cart-id");
  // Ищем ближайшеий input с количеством
  var $input = $(this).closest(".input-group").find(".number");
  // Берем значение количества товара
  var currentValue = parseInt($input.val());

  $input.val(currentValue + 1);

  // Запускаем функцию определенную ниже
  // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
  updateCart(cartID, currentValue + 1, 1, url);
});

function updateCart(cartID, quantity, change, url) {
  $.ajax({
    type: "POST",
    url: url,
    data: {
      cart_id: cartID,
      quantity: quantity,
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },

    success: function (data) {
      // Сообщение
      displayActionMessage(data);

      // Изменяем количество товаров в корзине
      var goodsInCartCount = $("#goods-in-cart-count");
      var cartCount = parseInt(goodsInCartCount.text() || 0);
      cartCount += change;
      goodsInCartCount.text(cartCount);

      // Меняем содержимое корзины
      var cartItemsContainer = $("#cart-items-container");
      cartItemsContainer.html(data.cart_items_html);
      
    },
  });
}
