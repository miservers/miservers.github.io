### Node.JS internals
Node.JS is server runtime mainly composed of google V8 engine and libuv. V8 compiles javascript code into a native machine code at runtime. 
libuv gives node.js access to the underlying server filesystem and UDP/TCP sockets.

*render()* function is called every time you want to render UI in the browser. 

### Install NodeJS on ubuntu 
~~~
wget -qO- https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt install -y nodejs
~~~

### Commandes
 
### Start/Stop node server

~~~
  node app.js
~~~

### Create a react Project

    npx create-react-app reactjs-demo

### start appli

    cd reactjs-demo
    npm start

### Install a module : NPM

    npm install --save react-router-dom
    
### Install all dependencies
defined in package.json

~~~
npm install
~~~

### create-react-app template

**advanced configuration**  
https://create-react-app.dev/docs/advanced-configuration

To define environment variables, create a file called **.env** in the root of your project.  
For example to change port from 3000 to 5000

~~~
//.env
PORT=5000

# other parameters
HOST=localhost

~~~
 


**Errors**   
unexpected end of json input while parsing near npx create-react-app   
--> solution : npm cache clear --force

### React ES6
#### Arrow functions
before 

~~~
sayHello = function() {
              return "Hello !";
}
~~~

with arrow

~~~
sayHello = () => {
            return "Hello ";
}
~~~
if parameter

~~~
sayHello = (name) => {
            return "Hello " + name;
}
~~~

#### this and Arrow functions
Arrow functions have no binding of **this**.  
With arrow functions, the **this**  represents the object that defined the arrow function.

### let var const
**let**: variable has a block scope, like Java.  
**var**: has a function scope. but not a block scope(visible outside a block).
**const** :  has a block scope. once created its value can never change.

### Components
Components are like JavaScript functions. They accept arbitrary inputs (called “props”) and return React elements describing what should appear on the screen.

~~~javascript
// Function components
function Welcome(props) {
  return <h1>Hello {props.name}</h1>;
}

// Class component
class Welcome extends React.Component {
  render() {
    return <h1>Hello {this.props.name}</h1>;
  }
}

// This component can bee used like
<Welcome   name="youssef"/> // display : Hello youssef
~~~

### Component lifecycle
 * **constructor(props)**
 * **render()**
 * **componentDidMount()**: invoked immediately after the component is insrted into the tree. If you need to load data from a remote endpoint, this is a good place to instantiate the network request. call **setState()** immediately in componentDidMount().
 * **componentDidUpdate()** . is invoked immediately after updating occurs. This is also a good place to do network requests

### Hooks
**useState** : create an new instance of **State** object.

~~~javascript
const MyFunctionCompenent = (props) => {
    let [name, setName] = useState('');
         
    return (
        <input type="text" onChange={(event) => setName(event.target.value)}></input>
        <h2>Hello {name}</h2>
    )
}
~~~

**useState of Array**

~~~js
const [biometrics, setBiometrics] = useState([]);

useEffect( () => { 
    async function fetchData () {
        ...                              
        setBiometrics(biometrics=>[...biometrics, metric]);      
    }
    fetchData();
}, []);
~~~

**useEffect** : like componentDidMount, this hook is called immediately after component creation. 
Syntax  

~~~
useEffect(sideEffectFunction, [stateToTrack]);

useEffect(() => {
  async function fetchData() {
    // You can await here
    const response = await MyAPI.getData(someId);
    // ...
  }
  fetchData();
}, [someId]); // Or [] if effect doesn't need props or state

~~~


**Example with Class and Hook**:

**With Class**:

~~~javascript
class Users extends React.Component {
  
  constructor (props){
    super(props);
    this.state = {users: [], selectedRow: -1,};
  }
  
  componentDidMount () {
    fetch ('http://127.0.0.1:8080/api/user')
      .then (response => response.json())
      .then (data => this.setState(state => state.users = data));
  }

 render () {
    
    return (
     <div>
      <ul>
        {this.state.users.map (user => <li>{user.username}</li>)}
      </ul>
      </div>
    )
  }
} 

export default Users;
~~~

**with Hook**: 

~~~javascript
import React , {useState, useEffect} from 'react';

const API_URL = 'http://127.0.0.1:8080/api/user';
  
export default function Users (props) {
  const [users, setUsers]       = useState([]); //users=[] empty table
  const [selectedRow, setSelectedRow] = useState(-1); 

  
  useEffect(()=> {
        loadData();
        }, []);
  
  const loadData = async () => {
                 await fetch (API_URL)
                    .then (response => response.json())
                    .then (data => setUsers(data)); 
                }
                
  return (
    <div>
      <ul>
      {users.map (user => <li>{user.username}</li>)}
      </ul>
    </div>
  );
} 
~~~


### material ui
 * https://github.com/mui-org/material-ui
 * https://material-ui.com/getting-started/templates/dashboard/
 
 * Grid : Material Design’s responsive UI is based on a 12-column grid layout.
### React UI Layout Grids
https://blog.bitsrc.io/12-react-ui-layout-grid-components-and-libraries-for-2019-16e8aa5d0b08
 * Grommet 
   ** https://storybook.grommet.io

### css3 Flexbox
Example

~~~
// CSS
.flex-container {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row-reverse;
}
To use it
<div class="flex-container">
...
</div>
~~~
### React CSS 
**Inline styles** : use camelCased for two names properties.Ex: **backgroundColor** instead of **background-color**.

~~~
function App() {

  const myStyle = {
     padding: '10px',
     border: '1px solid green',
     backgroundColor: "DodgerBlue",
  }

 return (
     return (
    <div className="App" style={myStyle}>
      <h2 style={{backgroundColor: "lightblue", color: "red"}}>List of Users</h2>
    </div>
  );
}
~~~

**Center a block**

~~~html
    <div style={{textAlign: "center"}}>
      <button type="button"> HELLOO </button>
    </div>
~~~

**Inline CSS with button:hover**

~~~js
const styles = {button:{width: '100%', 
                        height: '92px', 
                        background: 'red', 
                        margin: '8px 8px',
                        transition: 'all 0.1s ease-in',
                        "&:hover": {
                                    background: "#efefef"
                                    },
                        }};
~~~

**CSS file**: 

~~~
//App.css
.App-ListUsers {
  list-style-type: circle;
  color: aqua;
}
~~~
In App.js 

~~~
import './App.css';
...
function App() {
  return (
    <div className="App">
      <ul className="App-ListUsers">
        <ListUsers users={lusers} />
      </ul>
    </div> 
  );
~~~

**makeStyle from Material UI**

~~~javascript 
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme)=>({
  button: {
    flexGrow: 1,
    backgroundColor: "red"
  },
}));

export default function MedAppBar () {
  const classes = useStyles();
  
  return (
            <Button className={classes.button} color="primary">Login</Button>
    
~~~

### Props
Props are variables passed to component by its parent component.  
 * Props should never be changed in a child component. 
 * Props are equivalent to parameters of a pure javascript function.
 * Props are immutable.
 
~~~
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

<div className="App">
  <Welcome name="papa" />
</div>
~~~

### State
L’état local est réservé à l’interactivité, c’est-à-dire aux données qui évoluent dans le temps.
It is a object containing attributes of the class. use setState to update an attribute.   
[StateDemo.js](../java-workspace/reactjs-lab2/src/StateDemo.js)  

~~~javascript
 const styles = {margin: "10px"};

 class StateDemo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {product: '', price: 0, quantity: 0}
    }

    handleChange = (event) => {
        if (event.target.name == 'product')
            this.setState ({product: event.target.value})
        else if (event.target.name == 'price')
            this.setState ({price: event.target.value})
        
    } 

    render () {
        return (
            <div>
                <h2>State Demo</h2><hr/>
                Product:
                <input type="text" name="product" onChange={this.handleChange} style={styles}/>
                Price:
                <input type="text" name="price" onChange={this.handleChange} style={styles}/>
                <br/>
                <b>Added product: {this.state.product}, price: {this.state.price} DH</b>

            </div>
        );
    }
}
~~~

**Do Not Modify State Directly**  

~~~javascript
// Wrong
this.state.comment = 'Hello';

// Correct
this.setState({comment: 'Hello'});
~~~


**setState(function)**: a second form of setState() that accepts a function rather than an object.

~~~javascript
this.setState((state, props) => ({counter: state.counter + props.increment}));
~~~

### Lists
~~~
const lusers = [{id: 1, name: 'allal'}, 
                {id: 2, name: 'jilali'},
                {id: 3, name: 'boulam'}];
                
function ListUsers (props) {
      const listItems = props.users.map(user => <li key={user.id}>{user.name}</li>);
      return (
          {listItems}
  );
}

function App() {
  return (
    <div className="App">
        <ul className="App-ListUsers">
          <ListUsers users={lusers} />
        </ul>
        ...
~~~
     
### Forms

~~~
class SignupForm extends React.Component {

    handleSubmit = (event) => {
        event.preventDefault();

        const data = new FormData(event.target);

        const username = data.get('username').toLocaleLowerCase();        
        data.set ('username', username);

        fetch ('/services/signup', {
            method: 'POST',
            body: data,                                  
        }).then(response => console.log(response));
    }

    render () {
        return (
            <div>
            <form onSubmit={this.handleSubmit}>    
            <label> Username:
                <input type="text" name="username" id="username"></input>
            </label>
            <label> Email:
                <input type="email" name="email" id="email"></input>
            </label>
            <br />    
            <button type="submit" value="Submit" name="Submit" >Submit</button>
    
            </form>
            </div>

        );
    }
}
~~~

### Spaces
add {' '} to return block:

~~~javascript
      <Button variant="primary">primary</Button>{' '}
      <Button variant="success">success</Button>{' '}
~~~


### Tricks
**Export, Import var/const**
Export var/const 

~~~javascript
export var users = [ {}, {}, ];
~~~
Import var/const

~~~javascript
import {users} from './User';
~~~

### JSX

[jsx in depth](https://fr.reactjs.org/docs/jsx-in-depth.html)

**JSX code**

~~~javascript
<MyButton color="blue" shadowSize={2}>
  Cliquez ici
</MyButton>
~~~
is compiled to  :

~~~javascript
React.createElement(
  MyButton,
  {color: 'blue', shadowSize: 2},
  'Cliquez ici'
)
~~~

**Composant must start with Majuscule**:

~~~javascript
// incorrect!. write Hello insteed
function hello(props) {
  return <div>bonjour {props.toWhat}</div>;
}
~~~

**Spread Attributes**(**...**)
App1 and App2 are equivalent

~~~javascript
function App1() {
  return <Greeting firstName="wld" lastName="bni" />;
}

function App2() {
  const props = {firstName: 'wld', lastName: 'bni'};
  return <Greeting {...props} />;
}
~~~

### Modification of parent State by Child
~~~js
import React, {useState} from 'react';

export default function Parent() {
    const [address, setAddress ] = useState({street:'', city:''});

    const handler = (addr) => setAddress(addr);
    
    return (
      <div>
          <h2>Demo modification of state by Child</h2> 
              Address given by my child: {address.street + ' ' + address.city}
          <br/>
          <Child handler = {handler} />
       </div>
    );
  }
  
  function Child(props) {
    
      return (
        <button onClick = {() => props.handler({street:'12 rue imrane', city: 'casablanca'})}>
          I'm a child
        </button>
      );
  }
~~~

### Display Blob image
BLOB as string in JSON:

~~~js
<img className="pic__photo" src={"data:image/png;base64," + patient.picture.blob} />

OR 

avatar={<Avatar size={92} src={"data:image/png;base64," + patient.picture.blob}/>}
~~~

### Log an object on console
Use JSON.stringify():

~~~js
console.log("message: " + JSON.stringify(data));
~~~

### State/Hook: Add element to a table
~~~js
setPatients([new_patient,...patients]);
~~~ 

### Conditional rendring
[article](https://reactjs.org/docs/conditional-rendering.html)


### Coding Rules
 * Ditch the `var` keyword. Use only `let` and `const`. See this [article](https://programmingwithmosh.com/javascript/essential-modern-javascript-features/)

### React code style
https://github.com/airbnb/javascript/tree/master/react

 
### json-server : API to develop a Prototype  
**Install json-server**

~~~shell
npm install -g json-server 
~~~

**Define your Data in db.json file**

~~~json
{
    "Products": [
        {"category": "Sporting Goods", "price": "$49.99", "stocked": true, "name": "Football"},
        {"category": "Sporting Goods", "price": "$9.99", "stocked": true, "name": "Baseball"},
        {"category": "Sporting Goods", "price": "$29.99", "stocked": false, "name": "Basketball"},
        {"category": "Electronics", "price": "$99.99", "stocked": true, "name": "iPod Touch"},
        {"category": "Electronics", "price": "$399.99", "stocked": false, "name": "iPhone 5"},
        {"category": "Electronics", "price": "$199.99", "stocked": true, "name": "Nexus 7"}
    ],
    "users": [ 
        { "id": 1, "name": "Lorem ipsum"}, 
        { "id": 2, "name": "Taurex Aile"} 
     ] 
}  
~~~

**Start json-server**

~~~
json-server -p 2707 db.json
~~~

**Access to Resources**   
  * http://localhost:2707/Products  
  * http://localhost:2707/users  


### Tools 
 * `Visual Studio Code`
 * `json-server`
 * `RestMan`: opera extenstion to test an API 
 *  `react-devtools` : extention for chrome and firefox

### Best Libs/Modules
 * `material-ui` : it is compatible with React-bootstrap
 * `React-bootstrap` : React implementation of JQery Bootstrap
 * `React Router`
 * [**CLSX**](https://github.com/lukeed/clsx):  utility for constructing `className` strings conditionally.
 * `Redux`: global state managment
 * `SWR`  : Remote data fetching
 * `react-swipeable-views`: swipeable views


### React Bootstrap
Usage :

~~~javascript
import 'bootstrap/dist/css/bootstrap.min.css';

<TableContainer className="w-50 mx-auto">
   ...
~~~

### React Router
~~~
npm install react-router-dom
~~~

To switch to an Url use `Link`. Dont use `<a href...>` or `document.location.href`

~~~js
import {Link} from "react-router-dom";

<Link to={'/patient/record/' + record.id}>
  <img src={PatientRecordSvg} alt="Fiche patient"/>
</Link>
~~~ 

**URL Parameters : useParams**  

~~~js
// Patient.js : http://localhost:3000/patients/record/10004 
<Link to={'/patients/record/' + id} >
  <img src={PatientRecordSvg} alt="Fiche patient"/>
</Link>

// Routes.js
<Switch>
    <Route path="/patients/record/:id">
        <PatientRecord />
    </Route>
</Switch>


// PatientRecord.js
import React from 'react';
import {useParams} from 'react-router-dom';

export default function PatientRecord () {
  let {id} = useParams();
  
  return (
    <h2> Patient Record: {id} </h2> 
  );
}
~~~


### Material UI
 * Free templates : https://material-ui.com/getting-started/templates/
 * Tables : very good tables https://material-table.com/#/
 
** Custom a Button**

~~~html
<Button type="submit"  variant="contained" color="primary" style={{backgroundColor: 'green'}}>
~~~

### ANT Design
 * `pro-layout`


### Webpack
Webpack allow to  
 * use a loacl server
 * live reload
 * compile all sources into one exec file: perfs
 
 [getstarted with webpack: french] (https://www.alsacreations.com/tuto/lire/1754-debuter-avec-webpack.html)


### Less 
`Less` is a language extention for CSS. It aims to render CSS more dynamic: variables, functions etc. less files must be compiled into css, using less nodejs module, or in live by the browser using a special CDN javascript.   
Example

~~~css 
@background: #91d5ff;

.site-layout {
  background: @background;  
}
~~~


### Test your front-end against a real API
 * https://github.com/public-apis/public-apis
 * https://reqres.in/api/users
 * https://reqres.in



### Breakpoints, Grid(MUI)
Grid : subdivise screen into `12` columns.

[Default breakpoints](https://material-ui.com/customization/breakpoints/):  

 * xs : Phones. extra small  (<600px) devices
 * sm:  Tablet, Ipad. small (≥600px) 
 * md : Tablet large, Ipad pro. medium (≥960px), 
 * lg : Desktop. large device (≥1280px)
 * xl:  extra large(≥1920px)  
 
On ubuntu you can see screen width:  
  `$ xrandr | grep ' connected'`  => 1366x768 (277mm x 156mm): for my Lenovo x220 :  

### Media Query
#### react-responsive Library
~~~js
import { useMediaQuery } from 'react-responsive';
function PatientRecord () {
  const isDesktopOrLaptop = useMediaQuery({ minDeviceWidth: 1224 })
  const isTabletOrMobile = useMediaQuery({ maxWidth: 1224 })
  
  return (
     <Tabs ...
         tabPosition={isTabletOrMobile?'top':'left'}
     >

        ...

      </Tabs>
  )
~~~
 

### useMediaQuery
~~~js
import React from 'react';
import useMediaQuery from '@material-ui/core/useMediaQuery';

export default function SimpleMediaQuery() {
  const matches = useMediaQuery('(min-width:600px)'); //matches: true or false

  return <span>{`(min-width:600px) matches: ${matches}`}</span>;
}
~~~

### Hard Errors 
 * `Has been blocked by CORS policy  No 'Access-Control-Allow-Origin' header is present`  
   ==> Add **@CrossOrigin** on the spring controller class. 
   
 * `Error when installing a module: Unexpected end of JSON input while parsing near`  
   ==> npm cache clean --force

 * `Failed to execute 'json' on 'Response': body stream is locked`
    => json promise can be executed only once on this response object 

### Tools
  * **Postman**: HTTP requests builder. To test your API
  * **JSON server**: create a server to mock the backend 

### Run in Production mode
Compile the project:

~~~sh
  $ npm run build
~~~

Run serve

~~~sh
  $ sudo npm install -g serve
  $ serve -s build
 ~~~

### Icons
  * https://www.iconfinder.com/iconsets/hospital-19

### References
 * https://fr.reactjs.org/docs/
 * https://create-react-app.dev
 * https://www.w3schools.com/bootstrap
 * [Best React Libraries](https://www.robinwieruch.de/react-libraries)
 * [code style](https://github.com/airbnb/javascript/tree/master/react)
 * [React+Ant example](https://medium.com/wesionary-team/how-to-implement-ant-design-with-react-7d21b6e261cc)
 * [jsx in depth](https://fr.reactjs.org/docs/jsx-in-depth.html)
 * How to turn website to app: https://www.maketecheasier.com/turn-website-to-app-linux/
 * [Excellent article on CSS](https://css-tricks.com/snippets/css/a-guide-to-flexbox/#flexbox-background)
 
 
















