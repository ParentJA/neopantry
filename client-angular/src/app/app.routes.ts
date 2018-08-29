import { Routes } from '@angular/router';

import { LoggedIn } from './guards';
import {
  RecipeDetailResolver,
  RecipeListResolver,
  RecipeReviewResolver,
  UserRecipeListResolver
} from './resolvers';
import {
  HomeComponent,
  LogInComponent,
  RecipeComponent,
  RecipeDetailComponent,
  RecipeListComponent,
  RecipeReviewComponent,
  SignUpComponent,
  UserRecipeListComponent
} from './components';

export const ROUTES: Routes = [
  { path: 'sign-up', component: SignUpComponent },
  { path: 'log-in', component: LogInComponent },
  {
    path: 'recipe',
    component: RecipeComponent,
    children: [
      {
        path: ':id',
        component: RecipeDetailComponent,
        resolve: {
          recipe: RecipeDetailResolver
        }
      },
      {
        path: ':id/review',
        component: RecipeReviewComponent,
        resolve: {
          recipeReviews: RecipeReviewResolver
        }
      },
      {
        path: '',
        component: RecipeListComponent,
        resolve: {
          recipeData: RecipeListResolver
        }
      }
    ]
  },
  {
    path: 'user/:userId/recipe',
    component: UserRecipeListComponent,
    canActivate: [ LoggedIn ],
    resolve: {
      recipeData: UserRecipeListResolver
    }
  },
  { path: 'home', component: HomeComponent },
  { path: '', redirectTo: 'home', pathMatch: 'full' }
];
