import React, { useEffect, useState } from 'react';

import axios from 'axios';
import { sanitize } from 'dompurify';
import { Formik } from 'formik';
import { Breadcrumb, Button, Col, Container, Form, Image, Row } from 'react-bootstrap';
import { useParams } from 'react-router-dom';

import { getUser } from '../services/AuthService';
import { getRecipe } from '../services/RecipeService';

function RecipeDetail (props) {
  const params = useParams();

  const [recipe, setRecipe] = useState(null);

  useEffect(() => {
    const loadRecipe = async (id) => {
      const { response, isError } = await getRecipe(id);
      if (isError) {
        setRecipe(null);
      } else {
        setRecipe(response.data);
      }
    };
    loadRecipe(params.id);
  }, [params]);

  return (
    <Container className='pt-3'>
      <Breadcrumb>
        <Breadcrumb.Item href='/#/'>Home</Breadcrumb.Item>
        <Breadcrumb.Item href='/#/recipes'>Recipes</Breadcrumb.Item>
        <Breadcrumb.Item active>Recipe Detail</Breadcrumb.Item>
      </Breadcrumb>
      {recipe === null && <>Loading...</>}
      {
        recipe !== null && (
          <>
            <Image alt={recipe.name} fluid src={recipe.photo} />
            <h1>{recipe.name}</h1>
            <p>
              <span>{recipe.average_rating}/5</span><br />
              <span>Reviews ({recipe.num_reviews})</span>
            </p>
            <p>
              <span>{recipe.average_make_again}%</span><br />
              <span>Make it again</span>
            </p>
            <h2>Description</h2>
            <p dangerouslySetInnerHTML={{
              __html: `${recipe.description}`
            }}></p>
            <h2>Ingredients</h2>
            <p dangerouslySetInnerHTML={{__html: `${recipe.ingredients_text}`}}></p>
            <h2>Instructions</h2>
            <p dangerouslySetInnerHTML={{
              __html: `${recipe.instructions}`
            }}></p>
            <h2>My Review</h2>
            <h2>Reviews</h2>
          </>
        )
      }
    </Container>
  );
}

function MyNotes ({ recipe }) {
  const [isSubmitted, setSubmitted] = useState(false);

  const user = getUser();

  
}

function MyReview ({ recipe }) {
  const [isSubmitted, setSubmitted] = useState(false);

  const user = getUser();
  const reviews = recipe.reviews;
  const userReviews = reviews.find(review => review.id === user.id);
  const hasAddedReview = (userReviews.length > 0);

  const onSubmit = async (values, actions) => {
    const url = `/api/v1/recipes/reviews/`;
    const formData = new FormData();
    formData.append('make_again', values.make_again);
    formData.append('rating', values.rating);
    formData.append('review', values.review);
    try {
      await axios.post(url, formData);
      setSubmitted(true);
    } catch (response) {
      const data = response.response.data;
      for (const value in data) {
        actions.setFieldError(value, data[value].join(' '));
      }
    }
  };

  return (
    <>
      <h2>My Review</h2>
      <Formik
        initialValues={{
          makeAgain: '',
          rating: '',
          review: '',
        }}
        onSubmit={onSubmit}
      >
        {({
          errors,
          handleChange,
          handleSubmit,
          isSubmitting,
          setFieldValue,
          values
        }) => (
          <Form noValidate onSubmit={handleSubmit}>
            <Form.Group className='mb-3' controlId='makeAgain'>
              <Form.Label>Make again:</Form.Label>
              <Form.Control
                className={'make_again' in errors ? 'is-invalid' : ''}
                name='make_again'
                onChange={handleChange}
                required
                values={values.makeAgain}
              />
              {
                'make_again' in errors && (
                  <Form.Control.Feedback type='invalid'>{errors.make_again}</Form.Control.Feedback>
                )
              }
            </Form.Group>
            <Form.Group className='mb-3' controlId='rating'>
              <Form.Label>rating:</Form.Label>
              <Form.Control
                className={'rating' in errors ? 'is-invalid' : ''}
                name='rating'
                onChange={handleChange}
                required
                values={values.rating}
              />
              {
                'rating' in errors && (
                  <Form.Control.Feedback type='invalid'>{errors.rating}</Form.Control.Feedback>
                )
              }
            </Form.Group>
            <Form.Group className='mb-3' controlId='review'>
              <Form.Label>Review:</Form.Label>
              <Form.Control
                className={'review' in errors ? 'is-invalid' : ''}
                name='review'
                onChange={handleChange}
                required
                values={values.review}
              />
              {
                'review' in errors && (
                  <Form.Control.Feedback type='invalid'>{errors.review}</Form.Control.Feedback>
                )
              }
            </Form.Group>
            <div className='d-grid mb-3'>
              <Button 
                disabled={isSubmitting}
                type='submit' 
                variant='primary'
              >Submit
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </>
  );
}

export default RecipeDetail;
