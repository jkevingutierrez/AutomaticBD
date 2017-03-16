/*jshint esversion: 6 */

(function() {

    class Cierre {
        constructor() {}

        calcularCierre(variables, dependencias) {
            let cierre = [];
            let longitud = 0;

            if (variables instanceof Array && variables.length > 0) {
                cierre = variables.slice();
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
                        cierre.push(...dependencia.variablesImplicado);
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
            this.cierre = new Cierre();
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
                    let variablesAuxiliar = dependencia.variablesImplicante.slice();
                    for (let index = dependencia.variablesImplicante.length - 1; index >= 0; index--) {
                        let variable = variablesAuxiliar[index];
                        let variablesTemporales = variablesAuxiliar.filter((elem, j) => index !== j);

                        const cierreArray = this.cierre.calcularCierre(variablesTemporales, this.l1);
                        const contieneVariable = dependencia.variablesImplicado.every(elem => cierreArray.indexOf(elem) > -1);

                        if (contieneVariable) {
                            variablesAuxiliar.splice(index, 1);
                        }
                    }

                    const nuevaDependencia = new DependenciaFuncional(variablesAuxiliar, dependencia.variablesImplicado);
                    const existeNuevaDependencia = this.buscarDependencia(nuevaDependencia, this.l2);
                    if (!existeNuevaDependencia) {
                        this.l2.push(nuevaDependencia);
                    }
                }

            }

            return this.l2;
        }

        dependenciasRedundantes() {
            this.l3 = [];

            let l2Auxiliar = this.l2.slice().reverse();

            for (let index = this.l2.length - 1; index >= 0; index--) {
                let dependencia = l2Auxiliar[index];
                let dependenciasTemporales = l2Auxiliar.filter((elem, j) => index !== j);

                const cierreArray = this.cierre.calcularCierre(dependencia.variablesImplicante, dependenciasTemporales);
                const contieneVariable = dependencia.variablesImplicado.every(elem => cierreArray.indexOf(elem) > -1);

                const existeDependencia = this.buscarDependencia(dependencia, this.l3);
                if (contieneVariable) {
                    l2Auxiliar.splice(index, 1);
                } else if (!existeDependencia) {
                    this.l3.push(dependencia);
                }
            }

            return this.l3;
        }

        buscarDependencia(dependencia, dependencias) {
            const dependenciaEncontrada = dependencias.find(
                dependenciaActual =>
                dependenciaActual.variablesImplicado.equals(dependencia.variablesImplicado) &&
                dependenciaActual.variablesImplicante.equals(dependencia.variablesImplicante)
            );

            return dependenciaEncontrada ? true : false;
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

        const json2 = {
            t: ['a', 'b', 'c', 'd', 'e'],
            l: [{
                implicante: ['a'],
                implicado: ['b', 'd']
            }, {
                implicante: ['b'],
                implicado: ['c', 'd']
            }, {
                implicante: ['a', 'c'],
                implicado: ['e']
            }]
        };

        const json3 = {
            t: ['a', 'b', 'c', 'd', 'e'],
            l: [{
                implicante: ['a'],
                implicado: ['b']
            }, {
                implicante: ['b'],
                implicado: ['c']
            }, {
                implicante: ['c'],
                implicado: ['d']
            }, {
                implicante: ['d'],
                implicado: ['e']
            }, {
                implicante: ['e'],
                implicado: ['a']
            }, {
                implicante: ['a'],
                implicado: ['c']
            }, {
                implicante: ['c'],
                implicado: ['e']
            }, {
                implicante: ['e'],
                implicado: ['b']
            }, {
                implicante: ['b'],
                implicado: ['d']
            }, {
                implicante: ['d'],
                implicado: ['a']
            }]
        };

        const json4 = {
            t: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
            l: [{
                implicante: ['a'],
                implicado: ['b']
            }, {
                implicante: ['a', 'e'],
                implicado: ['d']
            }, {
                implicante: ['b'],
                implicado: ['c']
            }, {
                implicante: ['d', 'h'],
                implicado: ['c']
            }, {
                implicante: ['c'],
                implicado: ['d']
            }, {
                implicante: ['c', 'g'],
                implicado: ['b']
            }, {
                implicante: ['d'],
                implicado: ['a']
            }, {
                implicante: ['b', 'f'],
                implicado: ['a']
            }]
        };

        const json5 = {
            t: ['a', 'b', 'c', 'd', 'g', 'h'],
            l: [{
                implicante: ['a', 'b'],
                implicado: ['c']
            }, {
                implicante: ['b'],
                implicado: ['d']
            }, {
                implicante: ['d'],
                implicado: ['g', 'c']
            }, {
                implicante: ['c', 'g'],
                implicado: ['h']
            }]
        };

        const json6 = {
            t: ['a', 'b', 'c', 'd'],
            l: [{
                implicante: ['a'],
                implicado: ['b', 'c']
            }, {
                implicante: ['b'],
                implicado: ['c']
            }, {
                implicante: ['a'],
                implicado: ['b']
            }, {
                implicante: ['a', 'b'],
                implicado: ['c']
            }, {
                implicante: ['a', 'c'],
                implicado: ['d']
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
            implicante: ['c', 'f'],
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
        console.log(json6);

        const helper = new Conversor();
        const rt = helper.transformarART(json6);

        const l1 = rt.dependenciasElementales();
        const textoL1 = helper.transformarATexto(l1);
        console.log('L1:');
        console.log(textoL1);

        const l2 = rt.atributosExtranos();
        const textoL2 = helper.transformarATexto(l2);
        console.log('L2:');
        console.log(textoL2);

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
