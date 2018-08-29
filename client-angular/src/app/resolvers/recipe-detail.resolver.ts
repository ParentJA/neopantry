import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';

import { Observable } from 'rxjs';

import { RecipeForDetail, RecipeService } from '../services';

@Injectable()
export class RecipeDetailResolver implements Resolve<RecipeForDetail> {
  constructor(private recipeService: RecipeService) {}
  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<RecipeForDetail> {
    return this.recipeService.getRecipe(route.params.id);
  }
}
