import React, { useState } from 'react';
import { Formik } from 'formik';
import {
  Breadcrumb, Button, Card, Form
} from 'react-bootstrap';
import { Link, Navigate } from 'react-router-dom';

import { getUser } from '../services/AuthService';
import { updateProfile } from '../services/ProfileService';

function Profile (props) {
  const [isSubmitted, setSubmitted] = useState(false);
  const [profile, setProfile] = useState(getUser());

  const onSubmit = async (values, actions) => {
    try {
      const { response, isError } = await updateProfile(
        values.first_name,
        values.last_name,
        values.photo,
      );
      if (isError) {
        const data = response.data;
        for (const value in data) {
          actions.setFieldError(value, data[value].join(' '));
        }
      } else {
        setSubmitted(true);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Breadcrumb>
        <Breadcrumb.Item href='/#/'>Home</Breadcrumb.Item>
        <Breadcrumb.Item active>Profile</Breadcrumb.Item>
      </Breadcrumb>
      <Card>
        <Card.Header>Profile</Card.Header>
        <Card.Body>
          <Formik
            initialValues={{
              firstName: profile.first_name,
              lastName: profile.last_name,
              photo: [],
            }}
            onSubmit={onSubmit}
          >
            {({
              errors,
              handleChange,
              handleSubmit,
              isSubmitting,
              setFieldValue,
              values,
            }) => (
              <Form noValidate onSubmit={handleSubmit}>
                <Form.Group className='mb-3' controlId='firstName'>
                  <Form.Label>First name:</Form.Label>
                  <Form.Control
                    className={'firstName' in errors ? 'is-invalid' : ''}
                    name='firstName'
                    onChange={handleChange}
                    required
                    value={values.firstName}
                  />
                  {
                    'firstName' in errors && (
                      <Form.Control.Feedback type='invalid'>{errors.firstName}</Form.Control.Feedback>
                    )
                  }
                </Form.Group>
                <Form.Group className='mb-3' controlId='lastName'>
                  <Form.Label>Last name:</Form.Label>
                  <Form.Control
                    className={'lastName' in errors ? 'is-invalid' : ''}
                    name='lastName'
                    onChange={handleChange}
                    required
                    value={values.lastName}
                  />
                  {
                    'lastName' in errors && (
                      <Form.Control.Feedback type='invalid'>{errors.lastName}</Form.Control.Feedback>
                    )
                  }
                </Form.Group>
                <Form.Group className='mb-3' controlId='photo'>
                  <Form.Label>Photo:</Form.Label>
                  <Form.Control
                    className={'photo' in errors ? 'is-invalid' : ''}
                    name='photo'
                    onChange={event => {
                      setFieldValue('photo', event.currentTarget.files[0]);
                    }}
                    required
                    type='file'
                  />
                  {
                    'photo' in errors && (
                      <Form.Control.Feedback type='invalid'>{errors.photo}</Form.Control.Feedback>
                    )
                  }
                </Form.Group>
                <div className='d-grid mb-3'>
                  <Button
                    disabled={isSubmitting}
                    type='submit'
                    variant='primary'
                  >Update
                  </Button>
                </div>
              </Form>
            )}
          </Formik>
        </Card.Body>
      </Card>
    </>
  );
}

export default Profile;
