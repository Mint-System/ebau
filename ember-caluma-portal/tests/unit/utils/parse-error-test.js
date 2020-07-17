import AdapterError from "@ember-data/adapter/error";
import parseError from "ember-caluma-portal/utils/parse-error";
import { module, test } from "qunit";

module("Unit | Utility | parse-error", function () {
  test("it works", function (assert) {
    assert.equal(
      "Some error, Some other error",
      parseError(
        new AdapterError([
          {
            detail: "Some error",
            source: { pointer: "/foo/bar/non-field-errors" },
          },
          {
            detail: "Some other error",
            source: { pointer: "/foo/bar/non-field-errors" },
          },
          {
            detail: "Some field error",
            source: { pointer: "/foo/bar/some-field" },
          },
        ])
      )
    );
  });
});
