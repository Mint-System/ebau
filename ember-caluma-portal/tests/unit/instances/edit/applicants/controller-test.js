import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | instances/edit/applicants", function (hooks) {
  setupTest(hooks);

  // Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup(
      "controller:instances/edit/applicants"
    );
    assert.ok(controller);
  });
});
