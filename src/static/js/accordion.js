$( window ).on('load resize',function() {
   // Load goals on load.
   var w = $( window ).width()-121; // px
   $("#goals").width(w);

   // Switch only on click.
   var goals = document.getElementById('goals');
   var ideas = document.getElementById('ideas');
   var plans = document.getElementById('plans');
   goals.onclick = function() {
      $("#goals").width(w);
      $("#ideas").css({"width":"60px"});
      $("#plans").css({"width":"60px"});
   }
   ideas.onclick = function() {
      $("#goals").css({"width":"60px"});
      $("#ideas").width(w);
      $("#plans").css({"width":"60px"});
   }
   plans.onclick = function() {
      $("#goals").css({"width":"60px"});
      $("#ideas").css({"width":"60px"});
      $("#plans").width(w);
   }
});
