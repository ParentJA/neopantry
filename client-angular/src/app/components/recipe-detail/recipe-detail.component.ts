import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

import { RecipeForDetail } from '../../services';

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html'
})
export class RecipeDetailComponent implements OnInit {
  public recipe: RecipeForDetail;
  public noteForm: FormGroup;
  public reviewForm: FormGroup;

  constructor(private route: ActivatedRoute) {
    this.noteForm = new FormGroup({
      note: new FormControl('', Validators.required)
    });
    this.reviewForm = new FormGroup({
      review: new FormControl('', Validators.required)
    });
  }

  ngOnInit(): void {
    this.route.data.subscribe((data: {recipe: RecipeForDetail}) => this.recipe = data.recipe);
  }

  onDone(): void {}

  onSubmit(): void {}
}
