import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

import { RecipeData, RecipeService } from '../../services';

@Component({
  selector: 'app-recipe-list',
  templateUrl: './recipe-list.component.html'
})
export class RecipeListComponent implements OnInit {
  public searchControl: FormControl;
  public recipeData: RecipeData;

  constructor(
    private recipeService: RecipeService,
    private route: ActivatedRoute
  ) {
    this.searchControl = new FormControl('');
  }

  ngOnInit(): void {
    this.route.data.subscribe((data: {recipeData: RecipeData}) => this.recipeData = data.recipeData);
  }

  public search(): void {
    this.recipeService.getRecipes(1, this.searchControl.value).subscribe((recipeData: RecipeData) => this.recipeData = recipeData);
  }
}
