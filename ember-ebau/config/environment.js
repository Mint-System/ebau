"use strict";

const locales = require("./locales");

module.exports = function (environment) {
  // eslint-disable-next-line no-console
  console.log(
    `build env: APPLICATION: ${process.env.APPLICATION}, KEYCLOAK_HOST: ${process.env.KEYCLOAK_HOST}`
  );
  const app = process.env.APPLICATION || "kt_bern";
  const appConfig = {
    demo: {
      name: "demo",
      realm: "ebau",
    },
    kt_bern: {
      name: "be",
      realm: "ebau",
      allowApplicantManualWorkItem: false,
    },
    kt_uri: {
      name: "ur",
      realm: "urec",
      allowApplicantManualWorkItem: false,
    },
    kt_schwyz: {
      name: "sz",
      realm: "ebau",
      allowApplicantManualWorkItem: true,
    },
  }[app];
  const oidcHost = process.env.KEYCLOAK_HOST || "http://ebau-keycloak.local";

  const ENV = {
    modulePrefix: "ebau",
    environment,
    rootURL: "/",
    locationType: "auto",
    "ember-simple-auth-oidc": {
      host: `${oidcHost}/auth/realms/${appConfig.realm}/protocol/openid-connect`,
      clientId: "camac",
      authEndpoint: "/auth",
      tokenEndpoint: "/token",
      endSessionEndpoint: "/logout",
      userinfoEndpoint: "/userinfo",
      afterLogoutUri: "/login",
      loginHintName: "kc_idp_hint",
      enablePkce: true,
    },
    apollo: {
      apiURL: "/graphql/",
    },
    EmberENV: {
      FEATURES: {
        // Here you can enable experimental features on an ember canary build
        // e.g. EMBER_NATIVE_DECORATOR_SUPPORT: true
      },
      EXTEND_PROTOTYPES: {
        // Prevent Ember Data from overriding Date.parse.
        Date: false,
      },
    },

    APP: {
      // Here you can pass flags/options to your application instance
      // when it is created
    },

    languages: locales,
    fallbackLanguage: "de",

    APPLICATION: appConfig,
  };

  if (environment === "development") {
    // ENV.APP.LOG_RESOLVER = true;
    // ENV.APP.LOG_ACTIVE_GENERATION = true;
    // ENV.APP.LOG_TRANSITIONS = true;
    // ENV.APP.LOG_TRANSITIONS_INTERNAL = true;
    // ENV.APP.LOG_VIEW_LOOKUPS = true;
  }

  if (environment === "test") {
    // Testem prefers this...
    ENV.locationType = "none";

    // keep test console output quieter
    ENV.APP.LOG_ACTIVE_GENERATION = false;
    ENV.APP.LOG_VIEW_LOOKUPS = false;

    ENV.APP.rootElement = "#ember-testing";
    ENV.APP.autoboot = false;
  }

  if (environment === "production") {
    // here you can enable a production-specific feature
  }

  return ENV;
};
