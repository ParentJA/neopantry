import React from 'react';

import { Button, Card } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

function ResultListItem ({ result }) {
  return (
    <Card className='mb-3'>
      <Card.Img src={result.photo} variant='top' />
      <Card.Body>
        <Card.Title>{result.name}</Card.Title>
        <Card.Subtitle
          className='mb-2 text-muted'
        >{result.average_rating}/5 | Reviews ({result.num_reviews})
        </Card.Subtitle>
        <Card.Text>{result.short_description}</Card.Text>
        <div className='d-grid'>
          <LinkContainer to={`/recipes/${result.id}/`}>
            <Button variant='primary'>Detail</Button>
          </LinkContainer>
        </div>
      </Card.Body>
    </Card>
  );
}

export default ResultListItem;
