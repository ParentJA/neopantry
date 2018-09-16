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

export class RecipeNote {
  constructor(
    public id: number,
    public recipe: number,
    public user: number,
    public note: string
  ) {}

  static create(data: any): RecipeNote {
    return new RecipeNote(
      data.id,
      data.recipe,
      data.user,
      data.note
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

  static create(data: any): Recipe {
    return new Recipe(
      data.id,
      data.name,
      data.photo,
      data.average_rating,
      data.num_reviews,
      data.description,
      data.ingredients,
      data.instructions,
      data.average_make_again
    );
  }
}

export interface PaginatedData<T> {
  count: number;
  next: string;
  previous: string;
  results: T[];
}

export class RecipeData implements PaginatedData<Recipe> {
  constructor(
    public count: number,
    public next: string,
    public previous: string,
    public results: Recipe[]
  ) {}

  static create(data: any): RecipeData {
    return new RecipeData(
      data.count,
      data.next,
      data.previous,
      data.results.map((result: any) => Recipe.create(result))
    );
  }
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
      map((recipeData: any) => RecipeData.create(recipeData))
    );
  }

  getRecipe(id: number): Observable<RecipeForDetail> {
    return this.client.get(`/api/v1/recipes/${id}/`).pipe(
      map((recipe: any) => {
        return RecipeForDetail.create(recipe);
      })
    );
  }

  createRecipeNote(
    recipeId: number,
    userId: number,
    note: string
  ): Observable<RecipeNote> {
    const url = `/api/v1/recipes/notes/`;
    return this.client.post<RecipeNote>(url, {
      recipe: recipeId, user: userId, note
    }).pipe(
      map((recipeNoteData: any) => RecipeNote.create(recipeNoteData))
    );
  }

  getRecipeReviews(recipe: number = null, user: number = null): Observable<RecipeReview[]> {
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

  createRecipeReview(
    recipeId: number,
    userId: number,
    makeAgain: boolean,
    rating: number,
    review: string
  ): Observable<RecipeReview> {
    const url = `/api/v1/recipes/reviews/`;
    return this.client.post<RecipeReview>(url, {
      recipe: recipeId, user: userId, make_again: makeAgain, rating, review
    }).pipe(
      map((recipeReviewData: any) => RecipeReview.create(recipeReviewData))
    );
  }

  getUserRecipes(userId: number, page: number = 1): Observable<RecipeData> {
    let params: HttpParams = new HttpParams();
    params = params.set('page', page.toString());
    return this.client.get(`/api/v1/recipes/users/${userId}/recipes/`, {params}).pipe(
      map((recipeData: any) => RecipeData.create(recipeData))
    );
  }

  createUserRecipe(userId: number, recipeId: number): Observable<UserRecipe> {
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

  deleteUserRecipe(userId: number, recipeId: number): Observable<any> {
    return this.client.delete(`/api/v1/recipes/users/${userId}/recipes/${recipeId}/`);
  }
}
