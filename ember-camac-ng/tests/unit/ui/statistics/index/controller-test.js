import { setupTest } from "ember-qunit";
import { module, test } from "qunit";

module("Unit | Controller | statistics/index", function (hooks) {
  setupTest(hooks);

  // TODO: Replace this with your real tests.
  test("it exists", function (assert) {
    const controller = this.owner.lookup("controller:statistics/index");
    assert.ok(controller);
  });
});
