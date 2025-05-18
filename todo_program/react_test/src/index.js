import "bootstrap/dist/css/bootstrap.min.css";
import React, { useState,useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import axios from 'axios';
import { CardChecklist, Trash } from "react-bootstrap-icons";
import Container from "react-bootstrap/Container";
import FormControl from "react-bootstrap/FormControl";
import InputGroup from "react-bootstrap/InputGroup";
import Navbar from "react-bootstrap/Navbar";
import Button from 'react-bootstrap/Button';

//import reportWebVitals from './reportWebVitals';

async function fetchTodos() {
  try {
    console.log('開始獲取待辦事項...');
    const response = await axios.get('http://127.0.0.1:8000/api/todos',{
      withCredentials: true,
      headers: {
          'Content-Type': 'application/json',
      }
    });
    console.log('獲取成功:', response.data);
    return response.data;
  } 
  catch (error) {
    console.error('錯誤詳情:', {
      message: error.message,
      status: error.response?.status,
      data: error.response?.data,
      config: error.config
    });
    return [];
  }
}

function TodoItem(props) {
  return (
    <InputGroup key={props.id}>
      <InputGroup.Checkbox
        checked={props.completed}
        onChange={props.onToggle}
        />
        <FormControl
        value={props.title}
        onChange={(e) => props.onEdit(e.target.value)}
        style={{ textDecoration: props.completed ? 'line-through' : 'none' }}
        />

        <div style={{
          minWidth: '50px',  // 設定固定寬度
          display: 'flex',
          alignItems: 'center',  // 垂直置中
          padding: '0 15px',    // 左右間距
          color: '#6c757d'      // Bootstrap 的次要文字顏色
        }}>
          {props.time ? new Date(props.time).toLocaleString('zh-TW') : ''}
        </div>
        
        <Button variant="outline-danger" onClick={props.onDelete}>
          <Trash />
        </Button>
    </InputGroup>
  );
}

function App() {
  const [todos, setTodos] = useState([]);
  const [newTitle, setNewTitle] = useState('');
  
  useEffect(() => {
    async function loadTodos() {
      const data = await fetchTodos();
      setTodos(data);
    }
    loadTodos();
  }, []);
  
  async function addTodo() {
    if (!newTitle.trim()) return;
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/todos', {
        title: newTitle,
        completed: false,
      });
      setTodos([...todos, response.data]);
      setNewTitle('');
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  }

  async function deleteTodoFromServer(todoId) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/todos/${todoId}`);
      setTodos(todos.filter(t => t.id !== todoId));
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  }

  async function updateTodoStatus(todoId, completed) {
    try {
      const response = await axios.put(`http://127.0.0.1:8000/api/todos/${todoId}`, {
        completed: completed
      });
      setTodos(todos.map(t => t.id === todoId ? { ...t, completed: completed } : t));
    } catch (error) {
      console.error('Error updating todo status:', error);
    }
  }

  return (
    <>
      <Navbar bg="dark" variant="dark">
        <Container>
          <Navbar.Brand href="#home">
            <CardChecklist /> Todo List
          </Navbar.Brand>
        </Container>
      </Navbar>
      <Container>
        <input 
        type="text" 
        value={newTitle} 
        onChange={(e) => setNewTitle(e.target.value)} 
        placeholder="新增待辦事項" 
      />
        <button onClick={addTodo}>新增</button>

        <input type="search" placeholder="Search" />
        {todos.map((todo) => (
          <TodoItem 
            key={todo.id} 
            title={todo.title}
            completed={todo.completed}
            time={todo.time}

            onDelete={() => deleteTodoFromServer(todo.id)}
            
            onToggle={() => {
              updateTodoStatus(todo.id, !todo.completed);
            }}

            onEdit={(newTitle) => {
              setTodos(todos.map((t) => (t.id === todo.id ? { ...t, title: newTitle } : t)));
            }}
            />
        ))}
      </Container>
    </>
  );
}


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);



// onDelete={() => {setTodos(todos.filter((t) => t.id !== todo.id));}}
