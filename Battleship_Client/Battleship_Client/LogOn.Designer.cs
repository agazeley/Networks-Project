namespace Battleship_Client
{
    partial class LogOn
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.tb_ip = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.btn_logon = new System.Windows.Forms.Button();
            this.label3 = new System.Windows.Forms.Label();
            this.tb_name = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 30F);
            this.label1.Location = new System.Drawing.Point(9, 7);
            this.label1.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(264, 46);
            this.label1.TabIndex = 0;
            this.label1.Text = "BATTLESHIP";
            // 
            // tb_ip
            // 
            this.tb_ip.Location = new System.Drawing.Point(79, 80);
            this.tb_ip.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.tb_ip.Name = "tb_ip";
            this.tb_ip.Size = new System.Drawing.Size(76, 20);
            this.tb_ip.TabIndex = 1;
            this.tb_ip.Text = "127.0.0.1";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(22, 82);
            this.label2.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(54, 13);
            this.label2.TabIndex = 2;
            this.label2.Text = "Server IP:";
            // 
            // btn_logon
            // 
            this.btn_logon.Location = new System.Drawing.Point(158, 80);
            this.btn_logon.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.btn_logon.Name = "btn_logon";
            this.btn_logon.Size = new System.Drawing.Size(56, 19);
            this.btn_logon.TabIndex = 3;
            this.btn_logon.Text = "Log On";
            this.btn_logon.UseVisualStyleBackColor = true;
            this.btn_logon.Click += new System.EventHandler(this.btn_logon_Click);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(22, 59);
            this.label3.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(38, 13);
            this.label3.TabIndex = 5;
            this.label3.Text = "Name:";
            // 
            // tb_name
            // 
            this.tb_name.Location = new System.Drawing.Point(79, 57);
            this.tb_name.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.tb_name.Name = "tb_name";
            this.tb_name.Size = new System.Drawing.Size(76, 20);
            this.tb_name.TabIndex = 4;
            // 
            // LogOn
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(264, 108);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.tb_name);
            this.Controls.Add(this.btn_logon);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.tb_ip);
            this.Controls.Add(this.label1);
            this.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.Name = "LogOn";
            this.Text = "Log on and play!";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox tb_ip;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button btn_logon;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.TextBox tb_name;
    }
}

