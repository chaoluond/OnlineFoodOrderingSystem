/* Wait until the DOM loads by wrapping our code in a callback to $. */
$(function() {

  /* Add click event listeners to the restaurant list items. This adds a
   * handler for each element matching the CSS selector
   * .restaurant-list-item. */
  $('.menu').click(function(event) {
    
    /* Prevent the default link navigation behavior. */
    event.preventDefault();

    var $restaurant = $(this);
    var $menus = $restaurant.parents('.restaurant-list-item').find('.menu-sublist');


    /* Fade out all category-sublist.*/
    $('.category-sublist').slideUp();
   
    /* If the menu list is shown, hide it. */
    if($menus.is(':visible')) {
      $menus.slideUp();
      return;
    }

    /* Fade out all other menu lists. */
    $('.menu-sublist').not($menus).slideUp();


    /* Get the menus JSON data via Ajax. */
    $.ajax({
      type: 'GET',
      url: $restaurant.attr('href'),
      dataType: 'json'
    }).done(function(data) {

      /* This gets called if the Ajax call is successful. */

      /* We expect the JSON data to be in this form:
       *   [
       *     {
       *       "href": <url-of-category>,
       *       "name": <name-of-category>
       *     },
       *     ...
       *   ]
       */

      /* Empty out existing contents in the menu list. */
      $menus.empty();

      /* Add a list item/link for each menu received. */
      var menus = data;
      for(var i = 0, n = menus.length; i < n; ++i) {
        var menu = menus[i];
        $menus.append(
          $('<a>')
            .addClass('list-group-item no-gutter category')
            .attr('href', menu.href)
            .append(
              $('<div>')
                .text("Menu " + i + ": " + menu.name)
                .addClass('list-group-item-heading no-gutter')
            )
        );
      }
      /* Slide the newly populated category list into view. */
      $menus.slideDown();
    }).fail(function() {

      /* This gets called if the Ajax call fails. */

      $menus.empty().slideUp();

      /* Create an alert box. */
      var $alert = (
        $('<div>')
          .text('Whoops! Something went wrong.')
          .addClass('alert')
          .addClass('alert-danger')
          .addClass('alert-dismissible')
          .attr('role', 'alert')
          .prepend(
            $('<button>')
              .attr('type', 'button')
              .addClass('close')
              .attr('data-dismiss', 'alert')
              .html('&times;')
          )
          .hide()
      );
      /* Add the alert to the alert container. */
      $('#alerts').append($alert);
      /* Slide the alert into view with an animation. */
      $alert.slideDown();
    });
  });
});
