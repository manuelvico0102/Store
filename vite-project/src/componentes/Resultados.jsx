import React from "react";
import { Card } from "react-bootstrap";
import { Rating } from 'primereact/rating';



export default function Resultados({ products }) {
   
   return (
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "0.5rem" }}>
         {products.map((product) => (
            <Card key={product.id} style={{ width: "18rem" }}>
               <Card.Img variant="top" src={`images/${product.image}`} />
               <Card.Body>
                  <Card.Title>{product.title}</Card.Title>
                  <Rating value={product.rating.rate} cancel={false} />
                  <Card.Text style={{ textAlign: "left", marginTop: "auto" }}>{product.price}€</Card.Text>
               </Card.Body>
            </Card>
         ))}
      </div>
   );
}