// main.js
var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery');

var Nav = require('react-bootstrap/lib/Nav');
var Navbar = require('react-bootstrap/lib/Navbar');
var NavbarBrand = require('react-bootstrap/lib/NavbarBrand');
var NavbarHeader = require('react-bootstrap/lib/NavbarHeader');
var NavbarToggle = require('react-bootstrap/lib/NavbarToggle');
var NavbarBrand = require('react-bootstrap/lib/NavbarBrand');
var NavDropdown = require('react-bootstrap/lib/NavDropdown');
var NavItem = require('react-bootstrap/lib/NavItem');
var MenuItem = require('react-bootstrap/lib/MenuItem');
var Panel = require('react-bootstrap/lib/Panel');
var Table = require('react-bootstrap/lib/Table');
var Grid = require('react-bootstrap/lib/Grid');
var Row = require('react-bootstrap/lib/Row');
var Col = require('react-bootstrap/lib/Col');

var PrintJob = React.createClass({
    render: function() {
        var printerJobs = this.props.queue.map(function(job) {
            return (
                <tr>
                    <td>{job.queue_pos}</td>
                    <td>{job.user_id}</td>
                    <td>{job.filename}</td>
                </tr>
            );
        });
        return (
        <Table striped>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Username</th>
                    <th>Filename</th>
                </tr>
            </thead>
            <tbody> 
                {printerJobs}
            </tbody>
        </Table>
        );
    }
});

var PrinterPanel = React.createClass({
    render: function() {
        var printerNodes = this.props.data.map(function(printer) {
            return (
                <Col md={6}>
                    <Panel header={printer.name} key={printer.name}>
                        {function() { 
                            if (printer.queue.length != 0) {
                                return <PrintJob queue={printer.queue} key={printer.queue.filename} />
                            }
                            else {
                                return <p>Queue is currently empty.</p>
                            }
                        }.call(this)}
                    </Panel>
                </Col>
            );
        });
        return (
            <div className="printerPanel">
                {printerNodes}
            </div>
        );
    }
});

var PrinterPage = React.createClass({
    loadPrinterData: function() {
        $.ajax({
            url: this.props.url,
            dataType: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        });
    },
    getInitialState: function() {
        return {data: []};
    },
    componentDidMount: function() {
        this.loadPrinterData();
        setInterval(this.loadPrinterData, this.props.pollInterval);
    },
    render: function() {
        return (
            <div className="mainContent">
                <Navbar>
                    <NavbarHeader>
                        <NavbarBrand>
                            <a href="#">RPI PrinterQ</a>
                        </NavbarBrand>
                    <NavbarToggle />
                </NavbarHeader>
                <Nav pullRight>
                    <NavItem>Last updated: {this.state.data.last_updated}</NavItem>
                </Nav>
                </Navbar>
                <Grid>
                    <Row>
                            {/* Loading AJAX asynchronously, have to see if data.printers is defined first
                                before rendering */}
                            {this.state.data.printers && <PrinterPanel data={this.state.data.printers} />}
                    </Row>
                </Grid>
            </div>
        );
    }
});

ReactDOM.render(
    <PrinterPage url="/static/json/printers_data.json" pollInterval={20000} />,
    document.getElementById('container')
);
