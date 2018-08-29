import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';

import { Observable } from 'rxjs';

import { RecipeData, RecipeService } from '../services';

@Injectable()
export class RecipeListResolver implements Resolve<RecipeData> {
  constructor(private recipeService: RecipeService) {}
  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<RecipeData> {
    return this.recipeService.getRecipes();
  }
}
