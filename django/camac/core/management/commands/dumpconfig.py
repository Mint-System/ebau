from django.core.management.commands import dumpdata

config_models = {
    'core.ACheckquery',
    'core.ACirculationEmail',
    'core.ACirculationtransition',
    'core.ACopyanswer',
    'core.ACopyanswerMapping',
    'core.ACopydata',
    'core.ACopydataMapping',
    'core.ADeleteCirculation',
    'core.AEmail',
    'core.AFormtransition',
    'core.ALocation',
    'core.ALocationQc',
    'core.ANotice',
    'core.APageredirect',
    'core.APhp',
    'core.AProposal',
    'core.AProposalHoliday',
    'core.ASavepdf',
    'core.AValidate',
    'core.Action',
    'core.AirAction',
    'core.AnswerList',
    'core.AnswerQuery',
    'core.ArAction',
    'core.AttachmentExtension',
    'core.AttachmentExtensionRole',
    'core.AttachmentExtensionService',
    'core.AttachmentSection',
    'core.AttachmentSectionRole',
    'core.AttachmentSectionService',
    'core.Authority',
    'core.AuthorityAuthorityType',
    'core.AuthorityLocation',
    'core.AuthorityType',
    'core.AvailableAction',
    'core.AvailableInstanceResource',
    'core.AvailableResource',
    'core.BGroupAcl',
    'core.BRoleAcl',
    'core.BServiceAcl',
    'core.BillingAccount',
    'core.BillingAccountState',
    'core.BillingConfig',
    'core.BuildingAuthorityButton',
    'core.BuildingAuthorityDoc',
    'core.BuildingAuthorityEmail',
    'core.BuildingAuthoritySection',
    'core.Button',
    'core.Chapter',
    'core.ChapterPage',
    'core.ChapterPageGroupAcl',
    'core.ChapterPageRoleAcl',
    'core.ChapterPageServiceAcl',
    'core.CirculationAnswer',
    'core.CirculationAnswerType',
    'core.CirculationReason',
    'core.CirculationState',
    'core.CirculationType',
    'core.DocgenActivationAction',
    'core.DocgenActivationactionAction',
    'core.DocgenDocxAction',
    'core.DocgenPdfAction',
    'core.DocgenTemplate',
    'core.DocgenTemplateClass',
    'instance.Form',
    'core.FormGroup',
    'core.FormGroupForm',
    'instance.FormState',
    'user.Group',
    'user.GroupLocation',
    'core.InstanceResource',
    'core.InstanceResourceAction',
    'instance.InstanceState',
    'instance.InstanceStateDescription',
    'core.IrAllformpages',
    'core.IrCirculation',
    'core.IrEditcirculation',
    'core.IrEditcirculationSg',
    'core.IrEditformpage',
    'core.IrEditformpages',
    'core.IrEditletter',
    'core.IrEditletterAnswer',
    'core.IrEditnotice',
    'core.IrFormerror',
    'core.IrFormpage',
    'core.IrFormpages',
    'core.IrFormwizard',
    'core.IrGroupAcl',
    'core.IrLetter',
    'core.IrNewform',
    'core.IrPage',
    'core.IrRoleAcl',
    'core.IrServiceAcl',
    'core.Location',
    'core.Mapping',
    'core.NoticeType',
    'core.Page',
    'core.PageAnswerActivation',
    'core.PageForm',
    'core.PageFormGroup',
    'core.PageFormGroupAcl',
    'core.PageFormMode',
    'core.PageFormRoleAcl',
    'core.PageFormServiceAcl',
    'core.PublicationSetting',
    'core.Question',
    'core.QuestionChapter',
    'core.QuestionChapterGroupAcl',
    'core.QuestionChapterRoleAcl',
    'core.QuestionChapterServiceAcl',
    'core.QuestionType',
    'core.RFormlist',
    'core.RGroupAcl',
    'core.RList',
    'core.RListColumn',
    'core.RPage',
    'core.RRoleAcl',
    'core.RSearch',
    'core.RSearchColumn',
    'core.RSearchFilter',
    'core.RServiceAcl',
    'core.RSimpleList',
    'core.Resource',
    'core.Role',
    'core.Service',
    'core.ServiceAnswerActivation',
    'core.ServiceGroup',
    'core.WorkflowAction',
    'core.WorkflowItem',
    'core.WorkflowRole',
    'core.WorkflowSection',
}


class Command(dumpdata.Command):
    help = (
        "Output the camac configuration of the database as a fixture of the "
        " given format."
    )

    def handle(self, *app_labels, **options):
        options['indent'] = 2
        super().handle(*config_models, **options)
