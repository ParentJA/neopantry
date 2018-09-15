import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { RecipeData } from '../../services';

@Component({
  selector: 'app-user-recipe-list',
  templateUrl: './user-recipe-list.component.html'
})
export class UserRecipeListComponent implements OnInit {
  public query: string;
  public recipeData: RecipeData;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.data.subscribe((data: {recipeData: RecipeData}) => this.recipeData = data.recipeData);
  }
}
