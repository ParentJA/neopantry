import React, { useState } from 'react';

import axios from 'axios';
import { Formik } from 'formik';
import { Button, Col, Form, Row } from 'react-bootstrap';
import { AsyncTypeahead } from 'react-bootstrap-typeahead';

function Search ({ search }) {
  const [isLoading, setLoading] = useState(false);
  const [options, setOptions] = useState([]);

  const recipeSearchWord = async query => {
    if (query.length < 3) {
      setLoading(false);
      setOptions([]);
    } else {
      setLoading(true);
      try {
        const response = await axios({
          method: 'get',
          url: '/api/v1/recipes/recipe-search-words/',
          params: {
            query: query,
          }
        });
        setOptions(response.data);
      } catch(error) {
        console.error(error);
        setOptions([]);
      } finally {
        setLoading(false);
      }
    }
  };

  const onSubmit = async (values, actions) => {
    await search({
      limit: 10,
      offset: 0,
      query: values.query,
    });
  };

  return (
    <Formik
      initialValues={{
        country: '',
        points: '',
        query: '',
      }}
      onSubmit={onSubmit}
    >
      {({
        handleChange,
        handleSubmit,
        setFieldValue,
        values,
      }) => (
        <Form noValidate onSubmit={handleSubmit}>
          <Form.Group controlId='query'>
            <Form.Label>Query</Form.Label>
            <Col>
            <AsyncTypeahead
                filterBy={() => true}
                id="query"
                isLoading={isLoading}
                labelKey="word"
                name="query"
                onChange={selected => {
                  const value = selected.length > 0 ? selected[0].word : '';
                  setFieldValue('query', value);
                }}
                onInputChange={value => setFieldValue('query', value)}
                onSearch={recipeSearchWord}
                options={options}
                placeholder="Enter a search term (e.g. spicy)"
                type="text"
                value={values.query}
              />
              <Form.Text className='text-muted'>
                Searches for query in name and description.
              </Form.Text>
            </Col>
          </Form.Group>
          <Form.Group as={Row}>
            <Col>
              <Button type='submit' variant='primary'>Search</Button>
            </Col>
          </Form.Group>
        </Form>
      )}
    </Formik>
  );
}

export default Search;
