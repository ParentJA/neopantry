import React, { useState } from 'react';

import axios from 'axios';
import { Col, Container, Row } from 'react-bootstrap';

import Paginator from './Paginator';
import ResultList from './ResultList';
import Search from './Search';

function RecipeSearch (props) {
  const [paginatedData, setPaginatedData] = useState([]);

  const search = async (params) => {
    try {
      const response = await axios({
        method: 'get',
        url: '/api/v1/recipes/',
        params,
      });
      setPaginatedData(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Container className='pt-3'>
      <h1>Recipe Search</h1>
      <p className='lead'>
        Use the controls below to search the recipe catalog and filter the results.
      </p>
      <Row>
        <Col lg={4}>
          <Search search={search} />
        </Col>
        <Col lg={8}>
          {(paginatedData?.count ?? 0) > 0 && (
            <Paginator paginatedData={paginatedData} search={search} />
          )}
          <ResultList results={paginatedData?.results ?? []} />
        </Col>
      </Row>
    </Container>
  );
}

export default RecipeSearch;
