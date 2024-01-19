import { useEffect, useState } from "react";
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import Navegacion from './componentes/Navegacion';
import Resultados from './componentes/Resultados';
import './App.css'

function App() {
  const [products, setProducts] = useState([]);
  const [prods, setProds] = useState([]);

  function busquedaProductos(evt) {
    const nombre = evt.target.value.toLowerCase();
    console.log(nombre);
    setProds(products.filter(producto => producto.title.toLowerCase().includes(nombre)));
  }

  function filtrarProductos(filtro) {
    if(filtro != "Productos"){
      setProds(products.filter(producto => producto.category == filtro));
    }else
      setProds(products);
  }

  function ordenarProductos(filtro) {
    if(filtro === "PrecioMenor") {
      setProds([...products].sort((a, b) => a.price - b.price));
    } else if(filtro === "PrecioMayor") {
      setProds([...products].sort((a, b) => b.price - a.price));
    } else if(filtro === "OrdenarPuntuacionMenor") {
      setProds([...products].sort((a, b) => a.rating.rate - b.rating.rate));
    } else if(filtro === "OrdenarPuntuacionMayor") {
      setProds([...products].sort((a, b) => b.rating.rate - a.rating.rate));
    }
  }

  useEffect(() => {
    fetch(`http://localhost/api/productos?desde=0&hasta=100`)
      .then((response) => response.json())
      .then((products) => {
        setProducts(products);
        setProds(products);
      });
  }, []);

  return (
    <>
      <Navegacion handleBusquedas={busquedaProductos} filtrar={filtrarProductos} ordenar={ordenarProductos}/>
      <Resultados products={prods}/>
	  </>
  )
}

export default App
