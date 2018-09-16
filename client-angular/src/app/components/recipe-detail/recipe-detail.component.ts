import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

import { RecipeForDetail, RecipeReview, RecipeService, User } from '../../services';

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html'
})
export class RecipeDetailComponent implements OnInit {
  public recipe: RecipeForDetail;
  public reviews: RecipeReview[];
  public noteForm: FormGroup;
  public reviewForm: FormGroup;

  constructor(
    private route: ActivatedRoute,
    private recipeService: RecipeService
  ) {
    this.noteForm = new FormGroup({
      note: new FormControl('', Validators.required)
    });
    this.reviewForm = new FormGroup({
      makeAgain: new FormControl(false, Validators.required),
      rating: new FormControl(0, Validators.required),
      review: new FormControl('', Validators.required)
    });
  }

  ngOnInit(): void {
    this.route.data.subscribe((data: {recipe: RecipeForDetail}) => this.recipe = data.recipe);
    this.route.data.subscribe((data: {reviews: RecipeReview[]}) => this.reviews = data.reviews);
  }

  hasAddedReview(): boolean {
    return !!this.reviews.find(value => value.id === User.getUser().id);
  }

  hasAddedNote(): boolean {
    return false;
  }

  onDone(): void {
    this.recipeService.createRecipeReview(
      this.recipe.id,
      User.getUser().id,
      this.reviewForm.get('makeAgain').value,
      this.reviewForm.get('rating').value,
      this.reviewForm.get('review').value
    ).subscribe();
  }

  onSubmit(): void {
    this.recipeService.createRecipeNote(
      this.recipe.id,
      User.getUser().id,
      this.noteForm.get('note').value
    ).subscribe();
  }

  trackByReviews(index: number, review: RecipeReview): number {
    return review.id;
  }
}
