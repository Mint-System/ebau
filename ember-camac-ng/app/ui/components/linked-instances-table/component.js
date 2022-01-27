import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";

import config from "camac-ng/config/environment";

export default class LinkedInstancesTableComponent extends Component {
  @queryManager apollo;

  @service store;
  @service intl;
  @service shoebox;
  @service notification;
  @service fetch;

  @calumaQuery({ query: allCases, options: "options" }) casesQuery;

  get options() {
    return {
      pageSize: 15,
      processNew: (cases) => this.processNew(cases),
    };
  }

  get gqlFilter() {
    const filter = this.args.filter;
    const availableFilterSet = {
      buildingPermitType: {
        hasAnswer: [
          {
            question: "form-type",
            value: filter.buildingPermitType,
          },
        ],
      },
      instanceId: {
        metaValue: [
          {
            key: "camac-instance-id",
            value: filter.instanceId,
          },
        ],
      },
      dossierNumber: {
        metaValue: [
          {
            key: "dossier-number",
            lookup: "CONTAINS",
            value: filter.dossierNumber,
          },
        ],
      },
      intent: {
        searchAnswers: [
          {
            questions: config.APPLICATION.intentSlugs,
            lookup: "CONTAINS",
            value: filter.intent,
          },
        ],
      },
      caseStatus: {
        status: filter.caseStatus,
      },
      caseDocumentFormName: {
        documentForm: filter.caseDocumentFormName,
      },
    };

    const searchFilters = Object.entries(filter)
      .filter(
        ([key, value]) => Boolean(value) && Boolean(availableFilterSet[key])
      )
      .map(([key]) => availableFilterSet[key]);

    const workflow = this.args.workflow;
    return [...searchFilters, ...(workflow ? [{ workflow }] : [])];
  }

  get paginationInfo() {
    return htmlSafe(
      this.intl.t("global.paginationInfo", {
        count: this.casesQuery.value.length,
        total: this.casesQuery.totalCount,
      })
    );
  }

  async processNew(cases) {
    if (!cases.length) {
      return [];
    }
    const instanceIds = cases.map((_case) => _case.meta["camac-instance-id"]);

    await this.store.query("instance", {
      instance_id: instanceIds.join(","),
      include: "instance_state,user,form",
    });
    return cases;
  }

  get tableColumns() {
    return config.APPLICATION.caseTableColumns.linkedInstances;
  }

  get linkedAndOnSamePlot() {
    const dossierNumbers = this.args.instancesOnSamePlot.map(
      (instance) => instance.dossierNumber
    );
    return this.args.linkedDossiers
      .filter((value) => dossierNumbers.includes(value.dossierNumber))
      .map((instance) => instance.dossierNumber);
  }

  @action
  setup() {
    const camacFilters = {
      instance_state: this.args.filter.instanceState || "",
      location: this.args.filter.municipality,
    };
    this.casesQuery.fetch({
      order: config.APPLICATION.casesQueryOrder,
      filter: this.gqlFilter,
      queryOptions: {
        context: {
          headers: {
            "x-camac-filters": Object.entries(camacFilters)
              .filter(([, value]) => value)
              .map((entry) => entry.join("="))
              .join("&"),
          },
        },
      },
    });
  }

  @action
  loadNextPage() {
    this.casesQuery.fetchMore();
  }

  @action
  redirectToCase(caseRecord) {
    location.assign(
      `/index/redirect-to-instance-resource/instance-id/${caseRecord.instanceId}/`
    );
  }

  @dropTask
  *linkDossier(caseRecord) {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${caseRecord.instanceId}/link`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            data: {
              attributes: {
                "link-to": caseRecord.instanceId,
              },
            },
          }),
        }
      );

      this.fetchLinkedDossiers.perform(caseRecord);
      this.notification.success(
        this.intl.t("cases.miscellaneous.linkInstanceSuccess")
      );
    } catch (e) {
      this.notification.danger(
        this.intl.t("cases.miscellaneous.linkInstanceError")
      );
    }
  }

  @dropTask
  *unLinkDossier(caseRecord) {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${caseRecord.instanceId}/unlink`,
        {
          method: "PATCH",
          headers: { "content-type": "application/json" },
        }
      );
      this.fetchLinkedDossiers.perform(caseRecord);
      this.notification.success(
        this.intl.t("cases.miscellaneous.unLinkInstanceSuccess")
      );
    } catch (e) {
      this.notification.danger(
        this.intl.t("cases.miscellaneous.unLinkInstanceError")
      );
    }
  }

  @lastValue("fetchLinkedDossiers") linkedDossiers;
  @dropTask
  *fetchLinkedDossiers(caseRecord) {
    if (!caseRecord.instance.linkedInstances) {
      return null;
    }

    const instances = caseRecord.instance.linkedInstances.filter((instance) => {
      return instance.id !== caseRecord.instanceId;
    });

    instances.forEach((element) => element.fetchCaseMeta.perform());

    return yield instances;
  }
}
