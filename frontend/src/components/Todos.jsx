import React, { useEffect, useState } from "react";
import {
    Box,
    Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Text,
    useDisclosure
} from "@chakra-ui/react";


import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Checkbox from '@material-ui/core/Checkbox';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import UpdateIcon from '@material-ui/icons/Update';
import TextField from '@material-ui/core/TextField';

const TodosContext = React.createContext({
  todos: [], fetchTodos: () => {}
})

function AddTodo() {
    const [item, setItem] = React.useState("")
    const {todos, fetchTodos} = React.useContext(TodosContext)
  
    const handleInput = event  => {
        setItem(event.target.value)
    }
  
    const handleSubmit = (event) => {
        const newTodo = {
            "id": todos.length + 1,
            "item": item
        }
  
        fetch("http://localhost:8000/todo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newTodo)
        }).then(fetchTodos)
    }
  
    return (
        <form onSubmit={handleSubmit}>
            <TextField
                variant="outlined"
                placeholder="Add todo"
                margin="normal"
                direction="column"
                justify="center"
                alignItems="center"
                onChange={handleInput}
            />
        </form>
    )
}

function UpdateTodo({item, id}) {
    const {isOpen, onOpen, onClose} = useDisclosure()
    const [todo, setTodo] = useState(item)
    const {fetchTodos} = React.useContext(TodosContext)
  
    const updateTodo = async () => {
        await fetch(`http://localhost:8000/todo/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item: todo })
        })
        onClose()
        await fetchTodos()
    }
  
    return (
        <>
         <IconButton
            aria-label="Update"
            onClick={onOpen}
          >
            <UpdateIcon />
          </IconButton>
        <Modal isOpen={isOpen} onClose={onClose}>
            <ModalOverlay/>
            <ModalContent>
                <ModalHeader>Update Todo</ModalHeader>
                <ModalCloseButton/>
                <ModalBody>
                <InputGroup size="md">
                    <Input
                    pr="4.5rem"
                    type="text"
                    placeholder="Add a todo item"
                    aria-label="Add a todo item"
                    value={todo}
                    onChange={e => setTodo(e.target.value)}
                    />
                </InputGroup>
                </ModalBody>
  
            <ModalFooter>
            <Button h="1.5rem" size="sm" onClick={updateTodo}>Update Todo</Button>
            </ModalFooter>
        </ModalContent>
        </Modal>
    </>
    )
}



function DeleteTodo({id}) {
    const {fetchTodos} = React.useContext(TodosContext)
  
    const deleteTodo = async () => {
        await fetch(`http://localhost:8000/todo/${id}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: { "id": id }
        })
        await fetchTodos()
    }
  
    return (
        <IconButton
            aria-label="Delete"
            onClick={() => {
              deleteTodo(id);
            }}
          >
            <DeleteIcon />
          </IconButton>
    )
}


function TodoHelper({item, id, fetchTodos}) {
    return (
      <Box p={1} shadow="sm">
            <Text mt={4} as="div">
                <Flex align="end">
                <UpdateTodo item={item} id={id} fetchTodos={fetchTodos}/>
                <DeleteTodo id={id} fetchTodos={fetchTodos}/>
                </Flex>
            </Text>
      </Box>
    )
}

export default function Todos() {
  const [todos, setTodos] = useState([])
  const fetchTodos = async () => {
    const response = await fetch("http://localhost:8000/todo")
    const todos = await response.json()
    setTodos(todos.data)
  }
  useEffect(() => {
    fetchTodos()
  }, [])
  return (
    <List>
        <TodosContext.Provider value={{todos, fetchTodos}}>
            <AddTodo />
            {todos.map((todo) => (
                <ListItem dense button>
                    <Checkbox tabIndex={-1} disableRipple />
                    <ListItemText primary = {todo.item} />
                    <TodoHelper item={todo.item} id={todo.id} fetchTodos={fetchTodos} />
                    
                </ListItem>
            ))}
        </TodosContext.Provider>
    </List>
  )
}
