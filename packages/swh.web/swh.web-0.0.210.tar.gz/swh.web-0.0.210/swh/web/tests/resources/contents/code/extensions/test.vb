﻿Import System
Import System.IO
#Const DEBUG = True

Namespace Highlighter.Test
  ''' <summary>This is an example class.</summary>
  Public Class Program
    Protected Shared hello As Integer = 3
    Private Const ABC As Boolean = False

#Region "Code"
    ' Cheers!
    <STAThread()> _
    Public Shared Sub Main(ByVal args() As String, ParamArray arr As Object) Handles Form1.Click
      On Error Resume Next
      If ABC Then
        While ABC : Console.WriteLine() : End While
        For i As Long = 0 To 1000 Step 123
          Try
            System.Windows.Forms.MessageBox.Show(CInt("1").ToString())
          Catch ex As Exception       ' What are you doing? Well...
            Dim exp = CType(ex, IOException)
            REM ORZ
            Return
          End Try
        Next
      Else
        Dim l As New System.Collections.List<String>()
        SyncLock l
          If TypeOf l Is Decimal And l IsNot Nothing Then
            RemoveHandler button1.Paint, delegate
          End If
          Dim d = New System.Threading.Thread(AddressOf ThreadProc)
          Dim a = New Action(Sub(x, y) x + y)
          Static u = From x As String In l Select x.Substring(2, 4) Where x.Length > 0
        End SyncLock
        Do : Laugh() : Loop Until hello = 4
      End If
    End Sub
#End Region
  End Class
End Namespace
