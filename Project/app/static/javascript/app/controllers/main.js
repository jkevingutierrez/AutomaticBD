(function() {
    'use strict';

    angular
        .module('AutomaticBD')
        .controller('MainController', MainController);

    MainController.$inject = ['$scope', '$http', '$location'];

    /**
     * @namespace MainController
     */
    function MainController($scope, $http, $location) {
        var baseUrl = $location.absUrl();
        var vm = this;
        vm.hasFinishedLoading = true;

        vm.uploadFile = function($event) {
            console.log('upload');
            console.log($event);

            var files = $event.target.files; // FileList object

            // Loop through the FileList and render image files as thumbnails.
            for (var i = 0, f; f = files[i]; i++) {
                var reader = new FileReader();

                // Closure to capture the file information.
                reader.onload = (function(theFile) {
                    return function(e) {
                        var result = e.target.result;
                        var json = {};

                        try {
                            json = JSON.parse(result);
                        } catch (err) {
                            console.error(err);
                        }

                        console.log(json);
                        console.log(e);
                        console.log(theFile);
                    };
                })(f);

                // Read in the image file as a data URL.
                reader.readAsText(f);
            }
        };

        vm.initPanel = function() {
            function toggleChevron(e) {

                var $panelHeading = $(e.target).prev('.panel-heading');

                $panelHeading
                    .find('i.indicator')
                    .toggleClass('glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up');

                $panelHeading
                    .toggleClass('panel-blue');
            }

            $('#accordion').on('hidden.bs.collapse', toggleChevron);
            $('#accordion').on('shown.bs.collapse', toggleChevron);
            $('#accordion').click(function(e) {
                e.preventDefault();
            });

        };

        function main() {
            getJson();
        }

        function getJson() {
            $http({
                method: 'GET',
                url: baseUrl + 'static/resource/1.json'
            }).then(function(response) {
                var json = response.data;
                var jsonTest = {
                    variables: json.t,
                    dependencias: json.l
                };
                calculateMinimalCover(jsonTest);
            }).catch(function(error) {
                console.error(error);
            });
        }

        function calculateMinimalCover(json) {
            $http({
                method: 'POST',
                url: baseUrl + 'api',
                data: json
            }).then(function(response) {
                console.log(response);
                vm.solution = response.data;

                console.log(transformarATexto(vm.solution.l1));
                console.log(transformarATexto(vm.solution.l2));
                console.log(transformarATexto(vm.solution.l3));
            }).catch(function(error) {
                console.error(error);
            });
        }

        function transformarATexto(dependencias) {
            let textoDependencias = [];
            for (let dependencia of dependencias) {
                textoDependencias.push(dependencia.variablesImplicante.join('.') + ' -> ' + dependencia.variablesImplicado.join('.'));
            }

            return textoDependencias;
        }

        main();
    }

})();
