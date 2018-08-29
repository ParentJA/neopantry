import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export class Ingredient {
  constructor(
    public id: number,
    public description: string,
    public rank: number,
    public isOptional: boolean
  ) {}

  static create(data: any): Ingredient {
    return new Ingredient(
      data.id,
      data.description,
      data.rank,
      data.is_optional
    );
  }
}

export class RecipeForDetail {
  constructor(
    public id: number,
    public name: string,
    public description: string,
    public ingredients: Ingredient[],
    public instructions: string,
    public photo: string,
    public averageMakeAgain: number,
    public averageRating: number,
    public numReviews: number
  ) {}

  static create(data: any): RecipeForDetail {
    return new RecipeForDetail(
      data.id,
      data.name,
      data.description,
      data.ingredients.map((ingredient: any) => Ingredient.create(ingredient)),
      data.instructions,
      data.photo,
      data.average_make_again,
      data.average_rating,
      data.num_reviews
    );
  }
}

export class RecipeForList {
  constructor(
    public id: number,
    public name: string,
    public shortDescription: string,
    public photo: string,
    public averageMakeAgain: number,
    public averageRating: number,
    public numReviews: number
  ) {}

  static create(data: any): RecipeForList {
    return new RecipeForList(
      data.id,
      data.name,
      data.short_description,
      data.photo,
      data.average_make_again,
      data.average_rating,
      data.num_reviews
    );
  }
}

export class RecipeReview {
  constructor(
    public id: number,
    public recipe: number,
    public recipeName: string,
    public user: number,
    public userUsername: string,
    public makeAgain: boolean,
    public rating: number,
    public review: string
  ) {}

  static create(data: any): RecipeReview {
    return new RecipeReview(
      data.id,
      data.recipe,
      data.recipe_name,
      data.user,
      data.user_username,
      data.make_again,
      data.rating,
      data.review
    );
  }
}

export class UserRecipe {
  constructor(
    public id: number,
    public user: number,
    public recipe: any
  ) {}
}

export class Recipe {
  constructor(
    public id: number,
    public name: string,
    public photo: string,
    public averageRating: number,
    public numReviews: number,
    public description?: string,
    public ingredients?: Ingredient[],
    public instructions?: string,
    public averageMakeAgain?: number
  ) {}
}

export class RecipeData {
  constructor(
    public count: number,
    public next: string,
    public previous: string,
    public results: Recipe[]
  ) {}
}

@Injectable()
export class RecipeService {
  constructor(private client: HttpClient) {}

  getRecipes(page: number = 1, query: string = null): Observable<RecipeData> {
    let params: HttpParams = new HttpParams();
    params = params.set('page', page.toString());
    if (query) {
      params = params.set('query', query);
    }
    return this.client.get('/api/v1/recipes/', {params}).pipe(
      map((recipeData: any) => {
        return new RecipeData(
          recipeData.count,
          recipeData.next,
          recipeData.previous,
          recipeData.results.map((result: any) => {
            return new Recipe(
              result.id,
              result.name,
              result.photo,
              result.average_rating,
              result.num_reviews
            );
          })
        );
      })
    );
  }

  public getRecipe(id: number): Observable<RecipeForDetail> {
    return this.client.get(`/api/v1/recipes/${id}/`).pipe(
      map((recipe: any) => {
        return RecipeForDetail.create(recipe);
      })
    );
  }

  public getRecipeReviews(recipe: number = null, user: number = null): Observable<RecipeReview[]> {
    let params: HttpParams = new HttpParams();
    if (recipe) {
      params = params.set('recipe', recipe.toString());
    }
    if (user) {
      params = params.set('user', user.toString());
    }
    return this.client.get('/api/v1/recipes/reviews/', {params}).pipe(
      map((recipeReviews: any[]) => {
        return recipeReviews.map(recipeReview => RecipeReview.create(recipeReview));
      })
    );
  }

  public getUserRecipes(userId: number, page: number = 1): Observable<RecipeData> {
    let params: HttpParams = new HttpParams();
    params = params.set('page', page.toString());
    return this.client.get(`/api/v1/recipes/users/${userId}/recipes/`, {params}).pipe(
      map((recipeData: any) => {
        return new RecipeData(
          recipeData.count,
          recipeData.next,
          recipeData.previous,
          recipeData.results.map((result: any) => {
            const recipe = result.recipe;
            return new Recipe(
              recipe.id,
              recipe.name,
              recipe.photo,
              recipe.average_rating,
              recipe.num_reviews
            );
          })
        );
      })
    );
  }

  public createUserRecipe(userId: number, recipeId: number): Observable<UserRecipe> {
    return this.client.post(`/api/v1/recipes/users/${userId}/recipes/`, {recipe: recipeId}).pipe(
      map((userRecipe: any) => {
        return new UserRecipe(
          userRecipe.id,
          userRecipe.user,
          userRecipe.recipe
        );
      })
    );
  }

  public deleteUserRecipe(userId: number, recipeId: number): Observable<any> {
    return this.client.delete(`/api/v1/recipes/users/${userId}/recipes/${recipeId}/`);
  }
}
