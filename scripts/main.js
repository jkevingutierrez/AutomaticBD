/*jshint esversion: 6 */

(function() {

    class Cierre {
        constructor() {}

        calcularCierre(variables, dependencias) {
            let cierre = [];
            let longitud = 0;

            if (variables.indexOf('c') > -1 && variables.indexOf('f') > -1) {
                console.log('dependei');
                console.log(dependencias);
            }

            if (variables instanceof Array && variables.length > 0) {
                for (let variable of variables) {
                    cierre.push(variable);
                }
            } else if (typeof variables === 'string') {
                cierre.push(variables);
            }

            while (longitud < cierre.length) {
                longitud = cierre.length;
                const cierreInicial = cierre.slice();

                for (let dependencia of dependencias) {
                    const contieneVariables = dependencia.variablesImplicante.every(elem => cierre.indexOf(elem) > -1);
                    const variableImplicado = dependencia.variablesImplicado[0];

                    if (dependencia.variablesImplicante.length <= cierreInicial.length && contieneVariables && cierre.indexOf(variableImplicado) === -1) {
                        cierre.push(dependencia.variablesImplicado[0]);
                    }
                }
            }

            return cierre.sort();
        }

    }

    class Conversor {

        // transformarART(json) {
        //     const variables = json.t || [];
        //     const dependencias = json.l || [];
        //     let dependenciasFuncionales = [];
        //     for (let dependencia of dependencias) {
        //         if (typeof dependencia === 'string') {
        //             const dependenciaArray = dependencia.split(' -> ');

        //             if (dependenciaArray.length === 2) {
        //                 const implicante = dependenciaArray[0];
        //                 const implicado = dependenciaArray[1];
        //                 const variablesImplicante = implicante.split('.');
        //                 const variablesImplicado = implicado.split('.');

        //                 if (variablesImplicado.length > 0 && variablesImplicante.length > 0 ) {
        //                     const dependenciaFuncional = new DependenciaFuncional(variablesImplicante, variablesImplicado);
        //                     dependenciasFuncionales.push(dependenciaFuncional);
        //                 }
        //             }
        //         }
        //     }

        //     const rt = new RT(variables, dependenciasFuncionales);
        //     return rt;
        // }

        transformarART(json) {
            const variables = json.t || [];
            const dependencias = json.l || [];
            let dependenciasFuncionales = [];
            for (let dependencia of dependencias) {
                if (dependencia.implicante && dependencia.implicado && dependencia.implicante instanceof Array && dependencia.implicado instanceof Array && dependencia.implicante.length > 0 && dependencia.implicado.length > 0) {
                    const dependenciaFuncional = new DependenciaFuncional(dependencia.implicante, dependencia.implicado);
                    dependenciasFuncionales.push(dependenciaFuncional);
                }
            }

            const rt = new RT(variables, dependenciasFuncionales);
            return rt;
        }

        transformarATexto(dependencias) {
            let textoDependencias = [];
            for (let dependencia of dependencias) {
                textoDependencias.push(dependencia.variablesImplicante.join('.') + ' -> ' + dependencia.variablesImplicado.join('.'));
            }

            return textoDependencias;
        }
    }

    class DependenciaFuncional {
        constructor(variablesImplicante = [], variablesImplicado = []) {
            this.variablesImplicante = variablesImplicante;
            this.variablesImplicado = variablesImplicado;

            if (typeof variablesImplicado === 'string') {
                this.variablesImplicado = [variablesImplicado];
            }
        }
    }

    class RT {
        constructor(t, l) {
            this.t = t.sort();
            this.l = l;
            this.l1 = [];
            this.l2 = [];
            this.l3 = [];
        }

        buscarDependencia(dependencia, dependencias) {
            const dependenciaEncontrada = dependencias.find(
                dependenciaActual =>
                dependenciaActual.variablesImplicado.equals(dependencia.variablesImplicado) &&
                dependenciaActual.variablesImplicante.equals(dependencia.variablesImplicante)
            );

            return dependenciaEncontrada ? true : false;
        }

        dependenciasElementales() {
            this.l1 = [];
            this.l2 = [];
            this.l3 = [];

            for (let dependencia of this.l) {
                const existeDependencia = this.buscarDependencia(dependencia, this.l1);
                if (dependencia.variablesImplicado.length === 1 && !existeDependencia) {
                    this.l1.push(dependencia);
                } else {
                    for (let variable of dependencia.variablesImplicado) {
                        const nuevaDependencia = new DependenciaFuncional(dependencia.variablesImplicante, variable);
                        const existeNuevaDependencia = this.buscarDependencia(nuevaDependencia, this.l1);
                        if (!existeNuevaDependencia) {
                            this.l1.push(nuevaDependencia);
                        }
                    }
                }
            }

            return this.l1;
        }

        atributosExtranos() {
            this.l2 = [];
            this.l3 = [];

            for (let dependencia of this.l1) {
                const existeDependencia = this.buscarDependencia(dependencia, this.l2);

                if (dependencia.variablesImplicante.length === 1 && !existeDependencia) {
                    this.l2.push(dependencia);
                } else {
                    let longitud = dependencia.variablesImplicante.length;
                    let variablesTemporales = dependencia.variablesImplicante.slice();

                    for (let variable of dependencia.variablesImplicante) {

                    }
                }

            }

            return this.l2;
        }

        dependenciasRedundantes() {

            const l2Json = [{
                implicante: ['c'],
                implicado: ['a']
            }, {
                implicante: ['d'],
                implicado: ['e']
            }, {
                implicante: ['d'],
                implicado: ['f']
            }, {
                implicante: ['a', 'b'],
                implicado: ['c']
            }, {
                implicante: ['b', 'c'],
                implicado: ['d']
            }, {
                implicante: ['b', 'e'],
                implicado: ['c']
            }, {
                implicante: ['c' ,'f'],
                implicado: ['b']
            }, {
                implicante: ['c', 'f'],
                implicado: ['d']
            }, {
                implicante: ['c', 'd'],
                implicado: ['b']
            }, {
                implicante: ['c', 'e'],
                implicado: ['f']
            }].reverse();

            let dependencias = [];
            l2Json.forEach(function(dependencia) {
                const dependenciaFuncional = new DependenciaFuncional(dependencia.implicante, dependencia.implicado);
                dependencias.push(dependenciaFuncional);
            });

            this.l2 = dependencias.slice();
            this.l3 = [];

            let l2Auxiliar = this.l2.slice();
            const cierre = new Cierre();

            for (let index = this.l2.length - 1; index >= 0; index--) {
                let dependencia = l2Auxiliar[index];
                let dependenciasTemporales = l2Auxiliar.filter((test, j) => {
                    return index !== j;
                });

                const cierreArray = cierre.calcularCierre(dependencia.variablesImplicante, dependenciasTemporales);
                const contieneVariable = dependencia.variablesImplicado.every(elem => cierreArray.indexOf(elem) > -1);

                // console.log(dependenciasTemporales);
                // console.log(dependencia.variablesImplicante.join('.') + ' -> ' + dependencia.variablesImplicado.join('.'), contieneVariable);
                // console.log(cierreArray);

                const existeDependencia = this.buscarDependencia(dependencia, this.l3);
                if (contieneVariable) {
                    l2Auxiliar.splice(index, 1);
                } else if (!existeDependencia) {
                    this.l3.push(dependencia);
                }
            }

            return this.l3;
        }
    }


    function main() {
        // const json = {
        //     t: ['a', 'b', 'c', 'd', 'e', 'f'],
        //     l: ['a.b -> c', 'd -> e.f', 'c -> a', 'b.e -> c', 'b.c -> d' , 'c.f -> b.d', 'a.c.d -> b', 'c.e -> a.f']
        // };

        const json = {
            t: ['a', 'b', 'c', 'd', 'e', 'f'],
            l: [{
                implicante: ['a', 'b'],
                implicado: ['c']
            }, {
                implicante: ['d'],
                implicado: ['e', 'f']
            }, {
                implicante: ['c'],
                implicado: ['a']
            }, {
                implicante: ['b', 'e'],
                implicado: ['c']
            }, {
                implicante: ['b', 'c'],
                implicado: ['d']
            }, {
                implicante: ['c', 'f'],
                implicado: ['b', 'd']
            }, {
                implicante: ['a', 'c', 'd'],
                implicado: ['b']
            }, {
                implicante: ['c', 'e'],
                implicado: ['a', 'f']
            }]
        };

        const l1Json = [{
            implicante: ['a', 'b'],
            implicado: ['c']
        }, {
            implicante: ['c'],
            implicado: ['a']
        }, {
            implicante: ['b', 'c'],
            implicado: ['d']
        }, {
            implicante: ['b', 'e'],
            implicado: ['c']
        }, {
            implicante: ['a', 'c', 'd'],
            implicado: ['b']
        }, {
            implicante: ['d'],
            implicado: ['e']
        }, {
            implicante: ['d'],
            implicado: ['f']
        }, {
            implicante: ['c', 'f'],
            implicado: ['b']
        }, {
            implicante: ['c', 'f'],
            implicado: ['d']
        }, {
            implicante: ['c', 'e'],
            implicado: ['a']
        }, {
            implicante: ['c', 'e'],
            implicado: ['f']
        }];

        const l2Json = [{
                implicante: ['c'],
                implicado: ['a']
            }, {
                implicante: ['d'],
                implicado: ['e']
            }, {
                implicante: ['d'],
                implicado: ['f']
            }, {
                implicante: ['a', 'b'],
                implicado: ['c']
            }, {
                implicante: ['b', 'c'],
                implicado: ['d']
            }, {
                implicante: ['b', 'e'],
                implicado: ['c']
            }, {
                implicante: ['c' ,'f'],
                implicado: ['b']
            }, {
                implicante: ['c', 'f'],
                implicado: ['d']
            }, {
                implicante: ['c', 'd'],
                implicado: ['b']
            }, {
                implicante: ['c', 'e'],
                implicado: ['f']
            }];

        console.log('JSON Inicial:');
        console.log(json);

        const helper = new Conversor();
        const rt = helper.transformarART(json);

        const l1 = rt.dependenciasElementales();
        const textoL1 = helper.transformarATexto(l1);
        console.log('L1:');
        console.log(textoL1);

        // const l2 = rt.atributosExtranos();
        // const textoL2 = helper.transformarATexto(l2);
        // console.log('L2:');
        // console.log(textoL2);


        const l3 = rt.dependenciasRedundantes();
        const textoL3 = helper.transformarATexto(l3);
        console.log('L3:');
        console.log(textoL3);


        // const cierre = new Cierre();
        // const array = ['c', 'f'];
        // console.log('Cierre de', array);
        // console.log(cierre.calcularCierre(array, l1));
    }

    main();

}());
