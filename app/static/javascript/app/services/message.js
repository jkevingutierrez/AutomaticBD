(function() {
    'use strict';

    angular
        .module('AutomaticBD')
        .service('messages', MessagesService);

    MessagesService.$inject = ['alertify'];

    /**
     * @namespace MainController
     */
    function MessagesService(alertify) {
        this.error = function(error) {
            alertify.closeLogOnClick(false)
                .delay(5000)
                .error('<div class="message-wrapper"><div class="message-icon"><span class="glyphicon glyphicon-remove-circle" aria-hidden="true"></span></div><div class="message">' + error + '</div></div>');
        };

        this.success = function(message) {
            alertify.closeLogOnClick(false)
                .delay(5000)
                .success('<div class="message-wrapper"><div class="message-icon"><span class="glyphicon glyphicon-ok-circle" aria-hidden="true"></span></div><div class="message">' + message + '</div></div>');
        };
    }
})();
