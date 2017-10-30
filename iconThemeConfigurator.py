# encoding: utf-8

import gvsig
from gvsig.commonsdialog import msgbox
from gvsig.libs.formpanel import FormPanel

from org.gvsig.andami import PluginsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator
from org.gvsig.tools import ToolsLocator
from javax.swing import DefaultComboBoxModel
from javax.swing import DefaultListModel
from org.gvsig.andami.installer.icontheme import IconThemeInstallerFactory
from org.gvsig.installer.swing.api import SwingInstallerLocator

from java.io import File
from java.awt import BorderLayout

class IconThemeConfigurator(FormPanel):
  def __init__(self):
    FormPanel.__init__(self)
    self.load((__file__, "iconThemeConfigurator.xml"))
    self.setPreferredSize(800,400)
    self.load_icon_themes()
    self.initPackager()

  def showWindow(self):
    FormPanel.showWindow(self,"Icon theme Configurator")

  def btnCreate_click(self,*args):
    self.createTheme(
      self.txtCreateCode.getText(),
      self.txtCreateName.getText(),
      self.txtCreateAuthor.getText(),
      self.txtCreateURL.getText(),
      self.txtCreateDescription.getText()
    )

  def load_icon_themes(self):
    iconManager = ToolsSwingLocator.getIconThemeManager()
    iconManager.clear()
    cboModel = DefaultComboBoxModel()
    lstModel = DefaultListModel()
    cboModel.addElement("")
    lstModel.addElement("")
    for n in range(0,iconManager.getCount()):
      cboModel.addElement(iconManager.get(n))
      lstModel.addElement(iconManager.get(n))
    self.cboViewThemes.setModel(cboModel)
    self.lstThemes.setModel(lstModel)

  def createTheme(self, code, name, author, weburl, description):
    pluginsManager = PluginsLocator.getManager()
    iconManager = ToolsSwingLocator.getIconThemeManager()

    f = File(pluginsManager.getApplicationHomeFolder(),"icon-theme")
    if not f.exists() :
      f.mkdir()

    theme = iconManager.getDefault()
    f2 = File(f,code)
    if f2.exists() :
      msgbox("Icon theme '%s' already exists" % name)
      return
    saveid = theme.getID()
    theme.setID(code)
    theme.export(f)
    theme.setID(saveid)

    packageManager = ToolsLocator.getPackageManager()
    pkg = packageManager.createPackageInfo()
    pkg.setCode(code)
    pkg.setName(name)
    pkg.setDescription(description)
    pkg.setOwner(author)
    #pkg.setOwnerURL(weburl)
    pkg.setOfficial(False)
    pkg.setApplicationVersion(packageManager.createVersion("2.3.0"))
    packageManager.writePacakgeInfo(pkg,File(f2,"package.info"))
    self.load_icon_themes()
    msgbox("Icon theme '%s' created with default values." % name)

  def cboViewThemes_change(self, *args):
    theme = self.cboViewThemes.getSelectedItem()
    if theme in ("",None):
      return
    model = DefaultListModel()
    for iconName in theme.iterator():
      model.addElement(iconName)
    self.lstViewIcons.setModel(model)

  def lstViewIcons_change(self,*args):
    theme = self.cboViewThemes.getSelectedItem()
    iconName = self.lstViewIcons.getSelectedValue()
    icon = theme.getThemeIcon(iconName)
    self.txtViewName.setText(icon.getName())
    self.txtViewGroup.setText(icon.getGroup())
    self.txtViewLabel.setText(icon.getLabel())
    self.txtViewProvider.setText(icon.getProviderName())
    self.lblViewPreview.setText("")
    self.lblViewPreview.setIcon(icon.getImageIcon())

  def lstThemes_change(self,*args):
    theme = self.lstThemes.getSelectedValue()
    if theme in ("",None):
      return
    self.txtSelectName.setText(theme.getName())
    #self.txtSelectAuthor.setText(theme.xxx)
    #self.txtSelectURL.setText(theme.xxx)
    self.txtSelectDescription.setText(theme.getDescription())

  def initPackager(self):
    iconManager = ToolsSwingLocator.getIconThemeManager()
    pluginsManager = PluginsLocator.getManager()
    packageManager = ToolsLocator.getPackageManager()
    installerManager = SwingInstallerLocator.getSwingInstallerManager()
    packager = installerManager.createPackagerPanel(
        "icontheme", #IconThemeInstallerFactory.INSTALLER_NAME,
        File(pluginsManager.getApplicationHomeFolder(),"icon-theme"), #iconManager.getRepository().asFile(),
        pluginsManager.getInstallFolder()
    )
    packageInfo = packager.getPackageInfo()
    packageInfo.setArchitecture(packageManager.ARCH.ALL)
    packageInfo.setJavaVM(packageManager.JVM.J1_7)
    packageInfo.setOperatingSystem(packageManager.OS.ALL)
    packageInfo.setOfficial(False)
    packageInfo.setState(packageManager.STATE.TESTING)
    packageInfo.setType("icontheme") #IconThemeInstallerFactory.INSTALLER_NAME)
    packageInfo.setVersion(packageManager.createVersion("1.0.0"))
    self.packageContainer.setLayout(BorderLayout())
    self.packageContainer.add(packager,BorderLayout.CENTER)


def main(*args):
  manager = IconThemeConfigurator()
  manager.showWindow()
