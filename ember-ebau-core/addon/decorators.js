import { getOwner } from "@ember/application";
import { tracked } from "@glimmer/tracking";
import { confirm } from "ember-uikit";

export function loadingTask(target, property, desc) {
  const gen = desc.value;

  desc.value = function* (...args) {
    try {
      getOwner(this).lookup("controller:application").set("loading", true);

      return yield* gen.apply(this, args);
    } finally {
      getOwner(this).lookup("controller:application").set("loading", false);
    }
  };

  return desc;
}

export function objectFromQueryParams(filterConfig) {
  // There is no easy way of putting the fields directly into the queryParams array.
  // So you need to set the array yourself.
  return function (target, property, desc) {
    Object.keys(filterConfig).forEach((field) => {
      Object.defineProperty(
        target,
        field,
        tracked(target, field, {
          value: target[field],
          enumerable: true,
          configurable: true,
          writable: true,
          initializer: null,
        })
      );
    });

    delete desc.writable;
    delete desc.configurable;
    delete desc.initializer;
    delete desc.enumerable;

    desc.get = function () {
      return Object.entries(filterConfig).reduce(
        (serialized, [key, config]) => {
          const value = this[key];

          return {
            ...serialized,
            [key]:
              config.type === "select-multiple" ? value?.split(",") : value,
          };
        },
        {}
      );
    };
    desc.set = function (object) {
      Object.entries(filterConfig).forEach(([key, config]) => {
        const value = object[key];
        this[key] =
          config.type === "select-multiple" ? value?.join(",") : value;
      });
    };
    return desc;
  };
}

export function confirmTask(textOrKey) {
  return function (target, property, desc) {
    const gen = desc.value;

    desc.value = function* (...args) {
      const event = args.find((arg) => arg instanceof Event);

      if (event) {
        event.preventDefault();
      }

      const intl = getOwner(this).lookup("service:intl");
      const text = intl.exists(textOrKey) ? intl.t(textOrKey) : textOrKey;

      if (!(yield confirm(text))) {
        // confirmation was cancelled
        return;
      }

      return yield* gen.apply(this, args);
    };

    return desc;
  };
}

export default { loadingTask, confirmTask, objectFromQueryParams };
