import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, skip } from "qunit";

module("Integration | Component | dms/docs", function (hooks) {
  setupRenderingTest(hooks);

  skip("it renders", async function (assert) {
    // Set any properties with this.set('myProperty', 'value');
    // Handle any actions with this.set('myAction', function(val) { ... });

    await render(hbs`<Dms::Docs />`);

    assert.dom(this.element).hasText("");

    // Template block usage:
    await render(hbs`
      <Dms::Docs>
        template block text
      </Dms::Docs>
    `);

    assert.dom(this.element).hasText("template block text");
  });
});
