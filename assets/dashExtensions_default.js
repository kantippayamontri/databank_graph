window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(el) {
            setTimeout(function() {
                el.resize();
            }, 100); // Trigger resize after rendering
        }

    }
});