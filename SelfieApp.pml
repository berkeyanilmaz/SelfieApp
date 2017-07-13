<?xml version="1.0" encoding="UTF-8" ?>
<Package name="SelfieApp" format_version="4">
    <Manifest src="manifest.xml" />
    <BehaviorDescriptions>
        <BehaviorDescription name="behavior" src="behavior_1" xar="behavior.xar" />
    </BehaviorDescriptions>
    <Dialogs>
        <Dialog name="selfie" src="selfie/selfie.dlg" />
    </Dialogs>
    <Resources>
        <File name="main" src="main.py" />
        <File name="font-awesome" src="html/font-awesome.css" />
        <File name="social-media" src="html/social-media.html" />
    </Resources>
    <Topics>
        <Topic name="selfie_enu" src="selfie/selfie_enu.top" topicName="selfie" language="en_US" />
    </Topics>
    <IgnoredPaths />
    <Translations auto-fill="en_US">
        <Translation name="translation_en_US" src="translations/translation_en_US.ts" language="en_US" />
    </Translations>
</Package>
