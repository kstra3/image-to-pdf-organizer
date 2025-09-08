"""
Project management system for saving and loading image arrangements.

This module allows users to save their current image arrangements as projects
and load them later for continued work.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ProjectMetadata:
    """Metadata for a saved project."""
    name: str
    created: str
    modified: str
    description: str
    image_count: int
    version: str = "1.0"


@dataclass
class ProjectSettings:
    """Settings for PDF conversion."""
    page_size: str = "A4"
    compress: bool = False
    quality: int = 85
    watermark_text: str = ""
    watermark_position: str = "bottom-right"
    auto_rotate: bool = True


@dataclass
class ImageItem:
    """Individual image item in a project."""
    path: str
    original_path: str
    order: int
    enabled: bool = True
    rotation: int = 0
    brightness: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0


@dataclass
class Project:
    """Complete project data structure."""
    metadata: ProjectMetadata
    settings: ProjectSettings
    images: List[ImageItem]


class ProjectManager:
    """Manages saving and loading of projects."""
    
    def __init__(self, projects_dir: Optional[str] = None):
        """
        Initialize the project manager.
        
        Args:
            projects_dir: Directory to store projects (defaults to ./projects)
        """
        if projects_dir is None:
            projects_dir = os.path.join(os.path.dirname(__file__), "..", "..", "projects")
        
        self.projects_dir = os.path.abspath(projects_dir)
        
        # Create projects directory if it doesn't exist
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)
    
    def save_project(self, project: Project, filename: Optional[str] = None) -> str:
        """
        Save a project to disk.
        
        Args:
            project: Project data to save
            filename: Filename to save as (optional)
            
        Returns:
            str: Path to saved project file
        """
        if filename is None:
            # Generate filename from project name and timestamp
            safe_name = "".join(c for c in project.metadata.name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{timestamp}.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(self.projects_dir, filename)
        
        # Update modification time
        project.metadata.modified = datetime.now().isoformat()
        
        # Convert to dictionary
        project_dict = asdict(project)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(project_dict, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_project(self, filename: str) -> Project:
        """
        Load a project from disk.
        
        Args:
            filename: Name of project file to load
            
        Returns:
            Project: Loaded project data
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(self.projects_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Project file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            project_dict = json.load(f)
        
        # Convert back to Project object
        metadata = ProjectMetadata(**project_dict['metadata'])
        settings = ProjectSettings(**project_dict['settings'])
        images = [ImageItem(**img) for img in project_dict['images']]
        
        return Project(metadata=metadata, settings=settings, images=images)
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all available projects.
        
        Returns:
            List[Dict]: List of project summaries
        """
        projects = []
        
        if not os.path.exists(self.projects_dir):
            return projects
        
        for filename in os.listdir(self.projects_dir):
            if not filename.endswith('.json'):
                continue
                
            try:
                filepath = os.path.join(self.projects_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    project_dict = json.load(f)
                
                # Extract metadata
                metadata = project_dict.get('metadata', {})
                
                projects.append({
                    'filename': filename,
                    'name': metadata.get('name', 'Unnamed'),
                    'created': metadata.get('created', ''),
                    'modified': metadata.get('modified', ''),
                    'description': metadata.get('description', ''),
                    'image_count': metadata.get('image_count', 0),
                    'file_size': os.path.getsize(filepath)
                })
                
            except Exception as e:
                print(f"Warning: Could not read project {filename}: {e}")
                continue
        
        # Sort by modification date (newest first)
        projects.sort(key=lambda p: p['modified'], reverse=True)
        
        return projects
    
    def delete_project(self, filename: str) -> bool:
        """
        Delete a project file.
        
        Args:
            filename: Name of project file to delete
            
        Returns:
            bool: True if deleted successfully
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = os.path.join(self.projects_dir, filename)
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception:
            return False
    
    def export_project_summary(self, project: Project, output_path: str) -> str:
        """
        Export a human-readable project summary.
        
        Args:
            project: Project to export summary for
            output_path: Path to save summary
            
        Returns:
            str: Path to exported summary
        """
        summary = f"""
PROJECT SUMMARY
===============

Project Name: {project.metadata.name}
Description: {project.metadata.description}
Created: {project.metadata.created}
Last Modified: {project.metadata.modified}
Version: {project.metadata.version}

PDF SETTINGS
============
Page Size: {project.settings.page_size}
Compression: {'Enabled' if project.settings.compress else 'Disabled'}
Quality: {project.settings.quality}%
Auto-Rotate: {'Enabled' if project.settings.auto_rotate else 'Disabled'}
Watermark: {project.settings.watermark_text or 'None'}

IMAGES ({len(project.images)} total)
======
"""
        
        for i, img in enumerate(project.images, 1):
            status = "✓" if img.enabled else "✗"
            summary += f"{i:3d}. {status} {os.path.basename(img.path)}\n"
            if img.rotation != 0:
                summary += f"       Rotation: {img.rotation}°\n"
            if img.brightness != 1.0 or img.contrast != 1.0 or img.saturation != 1.0:
                summary += f"       Adjustments: B:{img.brightness:.1f} C:{img.contrast:.1f} S:{img.saturation:.1f}\n"
        
        # Save summary
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        return output_path
    
    def create_project_from_images(self, image_paths: List[str], name: str,
                                 description: str = "") -> Project:
        """
        Create a new project from a list of image paths.
        
        Args:
            image_paths: List of image file paths
            name: Project name
            description: Project description
            
        Returns:
            Project: New project object
        """
        # Create metadata
        now = datetime.now().isoformat()
        metadata = ProjectMetadata(
            name=name,
            created=now,
            modified=now,
            description=description,
            image_count=len(image_paths)
        )
        
        # Create default settings
        settings = ProjectSettings()
        
        # Create image items
        images = []
        for i, path in enumerate(image_paths):
            if os.path.exists(path):
                images.append(ImageItem(
                    path=path,
                    original_path=path,
                    order=i
                ))
        
        return Project(metadata=metadata, settings=settings, images=images)
