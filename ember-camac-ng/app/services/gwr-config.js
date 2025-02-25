import { action } from "@ember/object";
import Service, { inject as service } from "@ember/service";
import { getOwnConfig, macroCondition } from "@embroider/macros";

import ENV from "camac-ng/config/environment";

export default class GwrConfigService extends Service {
  @service session;
  @service shoebox;
  @service store;

  gwrAPI = "/housing-stat/regbl/api/ech0216/2";
  isTestEnvironment = ENV.appEnv !== "production";
  pageSize = 10;
  // Sorting currently not possible due to bug in GWR eCH-0216 API.
  // TODO: Re-add sorting once issue has been resolved.
  // projectSortColumn = "bau_modify_date";
  // projectSortDirection = "desc";
  // buildingSortColumn = "geb_modify_date";
  // buildingSortDirection = "desc";
  // quarterlyClosureSortColumn = "bau_create_date";
  // quarterlyClosureSortDirection = "desc";

  get modalContainer() {
    return ENV.APPLICATION.gwr.modalContainer ?? "#ember-camac-ng";
  }

  get importModels() {
    return ENV.APPLICATION.gwr.importModels;
  }

  get cantonAbbreviation() {
    return ENV.APPLICATION.gwr.cantonAbbreviation;
  }

  get authToken() {
    return this.session.data.authenticated.access_token;
  }

  get camacGroup() {
    return this.shoebox.content.groupId;
  }

  @action
  async fetchInstanceLinks(localIds) {
    const instances = await this.store.query("instance", {
      instance_id: [...new Set(localIds)].join(","),
    });

    return instances.map(({ id, identifier, dossierNumber, ebauNumber }) => ({
      localId: id,
      identifier: macroCondition(getOwnConfig().application === "be")
        ? ebauNumber
        : macroCondition(getOwnConfig().application === "sz")
        ? identifier
        : macroCondition(getOwnConfig().application === "ur")
        ? dossierNumber
        : "-",
      hostLink: `/index/redirect-to-instance-resource/instance-id/${id}?instance-resource-name=gwr&ember-hash=/gwr/${id}`,
    }));
  }
}
