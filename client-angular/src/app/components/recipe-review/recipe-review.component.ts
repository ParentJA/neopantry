import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { RecipeReview, RecipeService } from '../../services';

@Component({
  selector: 'app-recipe-review',
  templateUrl: './recipe-review.component.html'
})
export class RecipeReviewComponent implements OnInit {
  public query: string;
  public recipeReviews: RecipeReview[];
  constructor(
    private recipeService: RecipeService,
    private route: ActivatedRoute
  ) {}
  ngOnInit(): void {
    this.route.data.subscribe((data: {recipeReviews: RecipeReview[]}) => this.recipeReviews = data.recipeReviews);
  }
}
