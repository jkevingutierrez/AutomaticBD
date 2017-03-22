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

        vm.dependencies = [];

        vm.variables = [];

        vm.solution = {};

        vm.hasFinishedLoading = true;

        vm.hasErrors = false;

        vm.errorMessage = '';

        vm.uploadFile = uploadFile;

        vm.initPanel = initPanel;

        vm.calculateMinimalCover = calculateMinimalCover;

        vm.exportFile = exportFile;

        vm.closePoUp = closePopUp;

        vm.showPopUp = showPopUp;

        vm.clearFile = clearFile;

        function uploadFile($event) {
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
                        var json;

                        try {
                            vm.hasErrors = false;
                            json = JSON.parse(result);
                        } catch (error) {
                            vm.hasErrors = true;
                            vm.errorMessage = error;
                            console.error(error);
                        }

                        $scope.$apply(function() {
                            vm.initialJson = angular.copy(json);
                            vm.currentFile = {
                                name: theFile.name,
                                size: theFile.size,
                                type: theFile.type
                            };
                        });

                    };
                })(f);

                // Read in the image file as a data URL.
                reader.readAsText(f);
            }
        }

        function clearFile() {
            vm.hasErrors = false;
            vm.currentFile = undefined;
            vm.initialJson = undefined;
        }

        function initPanel() {
            function toggleChevron(e) {

                var $panelHeading = $(e.target).prev('.panel-heading');

                $panelHeading
                    .find('i.indicator')
                    .toggleClass('glyphicon glyphicon-chevron-down glyphicon glyphicon-chevron-up');
            }

            $('#accordion').on('hidden.bs.collapse', toggleChevron);
            $('#accordion').on('shown.bs.collapse', toggleChevron);
            $('#accordion').click(function(e) {
                e.preventDefault();
            });
        }

        function showPopUp($event) {
            var el = $event.currentTarget;
            $('#helpPopup').css({
                'left': el.offsetLeft - el.scrollLeft + 6,
                'top': el.offsetTop - el.scrollTop + 6
            });
            $('#helpPopup').toggle('fast');

        }

        function closePopUp() {
            $('#helpPopup').hide('fast');
        }

        function getJsonFromUrl(url) {
            $http({
                method: 'GET',
                url: url
            }).then(function(response) {
                if (response.data) {
                    var json = response.data;
                    var jsonTest = {
                        variables: json.t,
                        dependencias: json.l
                    };
                    vm.jsonExample = json;
                }
            }).catch(function(error) {
                console.error(error);
            });
        }

        function exportFile(json) {
            $http({
                method: 'POST',
                url: baseUrl + 'file',
                data: json
            }).then(function(response) {
                console.log(response);
                if (response.data) {
                    var json = response.data;
                    saveFile(JSON.stringify(json), 'test.json');
                }
            }).catch(function(error) {
                console.error(error);
            });
        }

        function saveFile(data, fileName) {
            var a = document.createElement("a");
            a.style = 'display: none';
            document.body.appendChild(a);
            var blob = new Blob([data], { type: 'octet/stream' });
            var url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = fileName;
            a.click();
            window.URL.revokeObjectURL(url);
        }

        function calculateMinimalCover(json) {
            $http({
                method: 'POST',
                url: baseUrl + 'api',
                data: json
            }).then(function(response) {
                console.log(response);
                if (response.data) {
                    vm.solution = {};
                    vm.solution = response.data;
                    saveFile(vm.solution.file, 'Recubrimiento.txt');

                    console.log(transform(vm.solution.l1));
                    console.log(transform(vm.solution.l2));
                    console.log(transform(vm.solution.l3));
                }
            }).catch(function(error) {
                console.error(error);
            });
        }

        function transform(dependencies) {
            var textArray = [];

            if (dependencies) {
                dependencies.forEach(function(dependency) {
                    textArray.push(dependency.variablesImplicante.join('.') + ' -> ' + dependency.variablesImplicado.join('.'));
                });
            }

            return textArray;
        }

        function main() {
            var resource = Math.floor((Math.random() * 6) + 1);
            console.log(resource);
            getJsonFromUrl(baseUrl + 'static/resource/' + resource + '.json');
        }


        main();
    }

})();
