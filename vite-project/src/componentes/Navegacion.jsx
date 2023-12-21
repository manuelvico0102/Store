import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

export default function Navegacion({ handleBusquedas, filtrar, ordenar}) {

    return (
        <Navbar expand="lg" className="bg-body-tertiary fixed-top">
            <Container fluid>
                <Navbar.Brand href="#">Tienda</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarScroll" />
                <Navbar.Collapse id="navbarScroll">
                    <Nav
                        className="me-auto my-2 my-lg-0"
                        style={{ maxHeight: '100px' }}
                        navbarScroll
                    >
                        <NavDropdown title="Categorias" id="navbarScrollingDropdown">
                            <NavDropdown.Item onClick={() => filtrar("men's clothing")}>Men's Clothing</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => filtrar("women's clothing")}>Women's Clothing</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => filtrar("jewelery")}>Jewelary</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => filtrar("electronics")}>Electronics</NavDropdown.Item>
                            <NavDropdown.Divider />
                            <NavDropdown.Item onClick={() => filtrar("Productos")}>Todos los productos</NavDropdown.Item>
                        </NavDropdown>
                        <NavDropdown title="Filtrar" id="navbarScrollingDropdown">
                            <NavDropdown.Item onClick={() => ordenar("PrecioMenor")}>Precio: Menor</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => ordenar("PrecioMayor")}>Precio: Mayor</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => ordenar("OrdenarPuntuacionMenor")}>Puntuación: Menor</NavDropdown.Item>
                            <NavDropdown.Item onClick={() => ordenar("OrdenarPuntuacionMayor")}>Puntuación: Mayor</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                    <Form className="d-flex">
                        <Form.Control
                            type="search"
                            placeholder="Search"
                            className="me-2"
                            aria-label="Search"
                            onChange={(evt) => handleBusquedas(evt)}
                        />
                        <Button variant="outline-success">Search</Button>
                    </Form>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}