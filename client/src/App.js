import React, { useState } from 'react';
import axios from 'axios';
import { Button, Container, Form, Nav, Navbar } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { Outlet, Route, Routes } from 'react-router-dom';

import Home from './components/Home';
import LogIn from './components/LogIn';
import Profile from './components/Profile';
import RecipeDetail from './components/RecipeDetail';
import Recipes from './components/Recipes';
import RecipeSearch from './components/RecipeSearch';
import SignUp from './components/SignUp';

import './App.css';

function App () {
  const [isLoggedIn, setLoggedIn] = useState(() => {
    return window.localStorage.getItem('neopantry.user') !== null;
  });

  const logIn = async (username, password) => {
    const url = `/api/v1/accounts/log-in/`;
    try {
      const response = await axios.post(url, { username, password });
      window.localStorage.setItem(
        'neopantry.user', JSON.stringify(response.data)
      );
      setLoggedIn(true);
      return { response, isError: false };
    } catch (error) {
      console.error(error);
      return { response: error, isError: true };
    }
  };

  const logOut = () => {
    window.localStorage.removeItem('neopantry.user');
    setLoggedIn(false);
  };

  return (
    <Routes>
      <Route
        path='/'
        element={
          <Layout isLoggedIn={isLoggedIn} logOut={logOut} />
        }
      >
        <Route index element={<Home isLoggedIn={isLoggedIn} />} />
        <Route
          path='sign-up'
          element={
            <SignUp isLoggedIn={isLoggedIn} />
          }
        />
        <Route
          path='log-in'
          element={
            <LogIn isLoggedIn={isLoggedIn} logIn={logIn} />
          }
        />
        <Route path='recipes' element={<Recipes />}>
          <Route index element={<RecipeSearch />} />
          <Route path=':id' element={<RecipeDetail />} />
        </Route>
        <Route 
          path='profile'
          element={
            <Profile />
          }
        />
      </Route>
    </Routes>
  );
}

function Layout ({ isLoggedIn, logOut }) {
  return (
    <>
      <Navbar bg='light' expand='lg' variant='light'>
        <Container>
          <LinkContainer to='/'>
            <Navbar.Brand>Neopantry</Navbar.Brand>
          </LinkContainer>
          <Navbar.Toggle />
          <Navbar.Collapse>
            <Nav className='me-auto'>
              <LinkContainer to='/recipes'>
                <Nav.Link>Recipes</Nav.Link>
              </LinkContainer>
              {
                isLoggedIn && (
                  <LinkContainer to='/profile'>
                    <Nav.Link>Profile</Nav.Link>
                  </LinkContainer>
                )
              }
            </Nav>
            {
              isLoggedIn && (
                <Form className='ms-auto'>
                  <Button type='button' onClick={() => logOut()}>Log out</Button>
                </Form>
              )
            }
          </Navbar.Collapse>
        </Container>
      </Navbar>
      <Container className='pt-3'>
        <Outlet />
      </Container>
    </>
  );
}

export default App;
