namespace Battleship_Client
{
    partial class MainForm
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
            this.dgv_lob = new System.Windows.Forms.DataGridView();
            this.game_id = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.num_players = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.btn_join = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.dgv_lob)).BeginInit();
            this.SuspendLayout();
            // 
            // dgv_lob
            // 
            this.dgv_lob.AllowUserToAddRows = false;
            this.dgv_lob.AllowUserToDeleteRows = false;
            this.dgv_lob.AllowUserToResizeColumns = false;
            this.dgv_lob.AllowUserToResizeRows = false;
            this.dgv_lob.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.dgv_lob.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.game_id,
            this.num_players});
            this.dgv_lob.Location = new System.Drawing.Point(43, 60);
            this.dgv_lob.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.dgv_lob.Name = "dgv_lob";
            this.dgv_lob.RowTemplate.Height = 24;
            this.dgv_lob.ScrollBars = System.Windows.Forms.ScrollBars.None;
            this.dgv_lob.Size = new System.Drawing.Size(407, 159);
            this.dgv_lob.TabIndex = 0;
            // 
            // game_id
            // 
            this.game_id.HeaderText = "Game ID";
            this.game_id.Name = "game_id";
            this.game_id.Width = 200;
            // 
            // num_players
            // 
            this.num_players.HeaderText = "Number of Players";
            this.num_players.Name = "num_players";
            this.num_players.Width = 300;
            // 
            // btn_join
            // 
            this.btn_join.Location = new System.Drawing.Point(388, 37);
            this.btn_join.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.btn_join.Name = "btn_join";
            this.btn_join.Size = new System.Drawing.Size(56, 19);
            this.btn_join.TabIndex = 1;
            this.btn_join.Text = "Join";
            this.btn_join.UseVisualStyleBackColor = true;
            this.btn_join.Click += new System.EventHandler(this.btn_join_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 24F);
            this.label1.Location = new System.Drawing.Point(37, 20);
            this.label1.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(129, 37);
            this.label1.TabIndex = 2;
            this.label1.Text = "Lobbies";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(494, 368);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.btn_join);
            this.Controls.Add(this.dgv_lob);
            this.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.Name = "MainForm";
            this.Text = "MainForm";
            ((System.ComponentModel.ISupportInitialize)(this.dgv_lob)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.DataGridView dgv_lob;
        private System.Windows.Forms.Button btn_join;
        private System.Windows.Forms.DataGridViewTextBoxColumn game_id;
        private System.Windows.Forms.DataGridViewTextBoxColumn num_players;
        private System.Windows.Forms.Label label1;
    }
}