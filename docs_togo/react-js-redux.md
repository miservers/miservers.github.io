
### Actions
Actions are payloads of information that send data from your application to your store. 

~~~js
{
  type: ADD_TODO,
  text: 'Build my first Redux app'
}
{ type: 'LIKE_ARTICLE', articleId: 42 }
~~~

Actions must have a `type` property that indicates the type of action being performed. 

You can call `store.dispatch(action)` from anywhere in your app

### Action Creators
Create Actions Objects.

~~~js
function addTodo(text) {
  return {
    type: ADD_TODO,
    text
  }
}
~~~

### Reducers
Reducer is a pure javascript function that takes the previous state and action, and returns the next state.

~~~js
(previousState, action) => nextState
~~~
Reducer Example:

~~~js
const todos = (state = [], action) => {
  switch (action.type) {
    case 'ADD_TODO':
      return [
        ...state,
        {
          id: action.id,
          text: action.text,
          completed: false
        }
      ]
    case 'TOGGLE_TODO':
      return state.map(todo =>
        (todo.id === action.id)
          ? {...todo, completed: !todo.completed}
          : todo
      )
    default:
      return state
  }
}
~~~

~~~js
import { combineReducers } from 'redux'

const todoApp = combineReducers({
  visibilityFilter,
  todos
})
~~~

### Store
Store :
 * Holds application state
 * Allows access to state via `getState()`
 * Allows state to be updated via `dispatch(action)`
 * Registers listeners via `subscribe(listener)`

~~~js
import { createStore } from 'redux'
import todoApp from './reducers'
const store = createStore(todoApp)
~~~
















