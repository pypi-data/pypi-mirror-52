import { AppState } from "@nteract/core";
import {
  epics as coreEpics,
  middlewares as coreMiddlewares,
  reducers
} from "@nteract/core";
import { applyMiddleware, combineReducers, compose, createStore } from "redux";
import { combineEpics, createEpicMiddleware, Epic } from "redux-observable";

const composeEnhancers =
  (window as any).__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

const rootReducer = combineReducers({
  app: reducers.app,
  comms: reducers.comms,
  config: reducers.config,
  core: reducers.core
});

export default function configureStore(initialState: Partial<AppState>) {
  const rootEpic = combineEpics<Epic>(...coreEpics.allEpics);
  const epicMiddleware = createEpicMiddleware();
  const middlewares = [epicMiddleware, coreMiddlewares.errorMiddleware];

  const store = createStore(
    rootReducer,
    // TODO: Properly type redux store for jupyter-extension
    (initialState as unknown) as any,
    composeEnhancers(applyMiddleware(...middlewares))
  );

  epicMiddleware.run(rootEpic);

  return store;
}
