#ifndef _GRAFO_H
#define _GRAFO_H
#include <stdlib.h>
#include <stdbool.h>
#include <stddef.h>
#include "lista.h"
#include "hash.h"
/* Primitivas para le grafo */

typedef struct grafo grafo_t;
typedef struct grafo_iter grafo_iter_t;
typedef bool (*grafo_visita_t) (const char* identificador, const hash_t* padre, const hash_t* orden, void* extra);
typedef struct grafo_recorrido{
    hash_t* padre; // hash con clave: id_vertice, valor: id de vertice que es su padre en el recorrido (NULL si no tiene padre)
    hash_t* orden; // hash con clave: id_vertice, valor: orden de dicho vertice en el recorrido
} grafo_recorrido_t;


//Crea un nuevo grafo, dirigido o no dirigido.
grafo_t* grafo_crear(bool es_dirigido, void (*destruir_dato) (void*));

//Destruye el grafo, liberando la memoria asociada.
//Pre: El grafo fue creado. La funcion de destruccion recibe el dato y lo destruye. En caso de recibir NULL, no se realizara operacion.
void grafo_destruir(grafo_t* grafo);

//Devuelve cantidad de vertices en el grafo
//Pre: El grafo fue creado
size_t grafo_cantidad(grafo_t* grafo);

//Devuelve una lista de identificadores de los vertices en el grafo. 
//Pre: El grafo fue creado
//Post: se devuelve una lista con los identificadores de los vertices (lista de const char*). 
//No deben destruirse los identificadores dentro de la lista resultante. 
lista_t* grafo_ids(grafo_t* grafo);

//Se agrega un vertice al grafo, con el identificador y valor asociado. En caso que ya existiera el vertice, se actualiza el dato asociado,
//destruyendo el anterior (si se recibio una funcion de destruccion al crearse el grafo).  
//Pre: El grafo fue creado. La cadena no es nula.
//Post: Se devuelve true en caso de haber podido crear el vertice, falso en caso contrario.
bool grafo_agregar_vertice(grafo_t* grafo, const char* identificador, void* dato);

//Se elimina el vertice al grafo, dado por el identificador. Se devuelve su valor asociado.
//Pre: El grafo fue creado. La cadena no es nula.
//Post: Se devuelve el dato asociado al vertice eliminado. NULL en caso de no existir dentro del grafo.
void* grafo_eliminar_vertice(grafo_t* grafo, char* identificador);

//Devuelve el valor asociado a un vertice
//Pre: El grafo fue creado
//Post: Devuelve el valor asociado al identificador. Devuelve NULL en caso que el identificador no corresponda a un vertice existente.
void* grafo_obtener(grafo_t* grafo, const char* identificador);

//Se crea una arista que va desde el primer identificador hasta el segundo. En caso que el grafo sea no dirigido, se creara la reciproca.
//Pre: El grafo fue creado
//Post: Si se pudo crear la arista, devuelve true, caso contrario false. Si alguno de los identificadores no son parte del grafo, devuelve false.
//En caso que ya existiera una arista que une dichos vertices, se pisa el peso asociado, no se crea otra arista (no se permiten redundancias). 
bool grafo_agregar_arista(grafo_t* grafo, const char* desde, const char* hasta, float peso);

//Se elimina una arista que va desde el primer identificador hasta el segundo. En caso que el grafo sea no dirigido, se elimina la reciproca.
//Pre: El grafo fue creado
//Post: en caso de existir dicha arista, se elimina y devuelve true, caso contrario false.
bool grafo_eliminar_arista(grafo_t* grafo, const char* desde, const char* hasta);

//Permite determinar si un identificador corresponde a un vertice del grafo.
//Pre: El grafo fue creado
//Post: true, en caso que pertenezca, false en otro caso.
bool grafo_pertenece(grafo_t* grafo, const char* identificador);

//Obtiene el peso de una arista que une dos vertices determinados.
//Pre: El grafo fue creado. Los identificadores son no-nulos.
//Post: En caso de no existir alguno de los identificadores como vertices del grafo, o que no exista una arista que una dichos vertices,
//devuelve false, y no se modifica el contenido del puntero 'peso'. En caso contrario, se guarda en 'peso' el valor del costo de la union,
//y devuelve true.
bool grafo_obtener_peso_arista(grafo_t* grafo, const char* desde, const char* hasta, float* peso);

//Obtiene una lista de vertices adyacentes al vertice dado.
//Pre: El grafo fue creado. El identificador es no-nulo.
//Post: Una lista con los identificadores de los vertices adyacentes al vertice identificado por el parametro dado (lista de const char*).
//No deben destruirse los identificadores dentro de la lista resultante. 
lista_t* grafo_adyacentes(grafo_t* grafo, const char* identificador);

//Obtiene una lista de componentes conexas del grafo, que se representan como listas de identificadores.
//Pre: El grafo fue creado, y es no dirigido.
//Post: se devuelve una lista de listas de identificadores (char*). Cada sub-lista tiene una copia los identificadores de una
//componente conexa del grafo. Por lo tanto, es necesario, para cada una de esas listas, liberar dichos identificadores. Si el 
//grafo era dirigido, se devuelve NULL. 
lista_t* grafo_componentes_conexas(grafo_t* grafo);

//Obtiene una lista con el camino de vertices (identificadores) que conducen desde el vertice origen, hasta el vertice destino (incluyendolos).
//Pre: El grafo fue creado. Los identificadores son no-nulos. La funcion Heuristica recibira por parametro:
//  void* datos_act: datos del vertice actual analizado.
//  void* datos_dest: datos del vertice destino. 
//En caso que la funcion heuristica sea NULL, se lo tratara como la funcion que devuelve 0 en todo caso. 
//Post: En caso que no exista camino entre los vertices, o alguno de ellos no exista en el grafo, devuelve NULL. Caso contrario, devuelve 
//la lista que representa el camino de 'origen' a 'destino'.
lista_t* grafo_camino_minimo(grafo_t* grafo, const char* origen, const char* destino, float (*heuristica) (void* datos_act, void* datos_dest)); 

//Devuelve un nuevo grafo que representa el arbol de tendido minimo del grafo recibido por parametro.
//Pre: El grafo fue creado, y es un grafo no dirigido.
grafo_t* grafo_mst(grafo_t* grafo);

//Devuelve una lista con un recorrido aleatorio de grafo, del largo indicado. Si origen es NULL, se comenzara desde un vertice aleatorio, sino desde dicho vertice.
//Si pesado es false, la probabilidad de movernos de un vertice a cualquiera de sus vecinos, es equiprobable, sino será directamente proporcional al peso de la arista.
//Pre: El grafo fue creado.
//Post: Se devuelve una lista con todos los vertices (identificadores) del recorrido, en el orden del recorrido. 
lista_t* grafo_random_walk(grafo_t* grafo, size_t largo, const char* origen, bool pesado);

//PRIMITIVAS DEL ITERADOR EXTERNO

//Crea un iterador de Grafo. No es necesario que siga algun tipo de recorrido (BFS o DFS).
//Pre: El grafo fue creado.
//Post: Un nuevo iterador de grafo, o NULL en caso que no se haya podido crear.
grafo_iter_t* grafo_iter_crear(grafo_t* iter);

//Devuelve si ya no hay mas identificadores para iterar.
//Pre: el iterador fue creado.
//Post: true en caso de encontrarse al final, false sino.
bool grafo_iter_al_final(grafo_iter_t* iter);

//Avanza el iterador a un siguiente identificador sin iterar.
//Pre: el iterador fue creado.
//Post: true, si pudo avanzar. false en caso que ya se encontrara al final. 
bool grafo_iter_avanzar(grafo_iter_t* iter);

//Obtiene el identificador actual en la iteracion.
//Pre: el iterador fue creado.
//Post: el identificador, o NULL en caso de encontrarse al final.
const char* grafo_iter_ver_actual(grafo_iter_t* iter);

//Libera la memoria asociada al iterador.
//Pre: el iterador de grafo fue creado.
void grafo_iter_destruir(grafo_iter_t* iter);


//PRIMITIVAS DE ITERADOR INTERNO:

//Itera con recorrido BFS al grafo. La funcion visitar recibe 4 parametros:
//  char* identificador:    el identificador del vertice 'actual' en el recorrido
//  hash_t* padre:          Hash cuya clave sea un identificador, y cuyo valor sea otro identificador, que corresponde al padre en el recorrido BFS
//  hash_t* orden:          Idem padre, pero cuyo valor sea el orden en el recorrido BFS de dicho vertice.
//  void* extra:            Puntero extra, que recibe por parametro la primitiva de iteracion
//const char* inicio:   vertice de inicio del recorrido. Se hace el recorrido desde este vertice (no se continua con vertices sin visitar). 
//Si es NULL, se recorren todas las componentes del grafo. Si el vertice de origen es indicado, pero no existe en el grafo, se devuelve NULL.
grafo_recorrido_t* grafo_iterar_bfs(grafo_t* grafo, grafo_visita_t visitar , void* extra, const char* inicio);

//Itera con recorrido DFS al grafo. La funcion visitar recibe 4 parametros:
//  char* identificador:    el identificador del vertice 'actual' en el recorrido
//  hash_t* padre:          Hash cuya clave sea un identificador, y cuyo valor sea otro identificador, que corresponde al padre en el recorrido DFS
//  hash_t* orden:          Idem padre, pero cuyo valor sea el orden en el recorrido DFS de dicho vertice.
//  void* extra:            Puntero extra, que recibe por parametro la primitiva de iteracion
//const char* inicio:   vertice de inicio del recorrido. Se hace el recorrido desde este vertice (no se continua con vertices sin visitar).
//Si es NULL, se recorren todas las componentes del grafo. Si el vertice de origen es indicado, pero no existe en el grafo, se devuelve NULL.
grafo_recorrido_t* grafo_iterar_dfs(grafo_t* grafo, grafo_visita_t visitar , void* extra, const char* origen);

#endif // _GRAFO_H
